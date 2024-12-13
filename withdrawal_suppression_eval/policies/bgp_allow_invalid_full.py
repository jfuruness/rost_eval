from typing import TYPE_CHECKING, Optional

from bgpy.simulation_engine import BGPFull

if TYPE_CHECKING:
    from bgpy.shared.enums import Relationships
    from bgpy.simulation_engine.ann_containers import AnnInfo, SendInfo
    from bgpy.simulation_engine.announcement import Announcement as Ann
    from bgpy.simulation_framework import Scenario


class BGPAllowInvalidFull(BGPFull):
    error_on_invalid_routes = False

    def process_incoming_anns(
        self: "BGPFull",
        *,
        from_rel: "Relationships",
        propagation_round: int,
        # Usually None for attack
        scenario: "Scenario",
        reset_q: bool = True,
    ):
        """Process all announcements that were incoming from a specific rel"""

        for prefix, anns in self.recv_q.items():
            # Get announcement currently in local rib
            local_rib_ann: Ann | None = self.local_rib.get(prefix)
            current_ann: Ann | None = local_rib_ann
            current_processed: bool = True

            # For each announcement that is incoming
            for ann in anns:
                # withdrawals
                err = "Recieved two withdrawals from the same neighbor"
                assert len([x.as_path[0] for x in anns if x.withdraw]) == len(
                    {x.as_path[0] for x in anns if x.withdraw}
                ) and self.error_on_invalid_routes, err

                err = (
                    f"{self.as_.asn} Recieved two NON withdrawals "
                    f"from the same neighbor {anns}"
                )
                assert len(
                    [(x.as_path[0], x.next_hop_asn) for x in anns if not x.withdraw]
                ) == len(
                    {(x.as_path[0], x.next_hop_asn) for x in anns if not x.withdraw}
                ) and self.error_on_invalid_routes, err

                # Always add to ribs in if it's not a withdrawal
                if not ann.withdraw:
                    err = (
                        "you should never be replacing anns. "
                        "You should always withdraw first, "
                        "have it be blank, then add the new one"
                    )
                    assert (
                        self.ribs_in.get_unprocessed_ann_recv_rel(ann.as_path[0], prefix)
                        is None
                    ) and self.error_on_invalid_routes, str(self.as_.asn) + " " + str(ann) + err

                    self.ribs_in.add_unprocessed_ann(ann, from_rel)
                # Process withdrawals even for invalid anns in the ribs_in
                if ann.withdraw:
                    if self._process_incoming_withdrawal(ann, from_rel):
                        # the above will return true if the local rib is changed
                        updated_loc_rib_ann: Ann | None = self.local_rib.get(prefix)
                        if current_processed:
                            current_ann = updated_loc_rib_ann
                        else:
                            assert updated_loc_rib_ann, "mypy type check"
                            new_ann_is_better: bool = self._new_ann_better(
                                current_ann,
                                current_processed,
                                from_rel,
                                updated_loc_rib_ann,
                                True,
                                updated_loc_rib_ann.recv_relationship,
                            )
                            if new_ann_is_better:
                                current_ann = updated_loc_rib_ann
                                current_processed = True

                # If it's valid, process it
                elif self._valid_ann(ann, from_rel):
                    # Announcement will never be overriden, so continue
                    if getattr(current_ann, "seed_asn", None):
                        continue

                    new_ann_is_better = self._new_ann_better(
                        current_ann, current_processed, from_rel, ann, False, from_rel
                    )

                    # If the new priority is higher
                    if new_ann_is_better:
                        current_ann = ann
                        current_processed = False

            if local_rib_ann is not None and local_rib_ann is not current_ann:
                # Best ann has already been processed

                withdraw_ann: Ann = local_rib_ann.copy(
                    overwrite_default_kwargs={"withdraw": True, "seed_asn": None}
                )

                self._withdraw_ann_from_neighbors(withdraw_ann)
                err = f"withdrawing ann that is same as new ann {withdraw_ann}"
                if not current_processed:
                    assert current_ann is not None, "mypy type check"
                    assert not withdraw_ann.prefix_path_attributes_eq(
                        self._copy_and_process(current_ann, from_rel)
                    ) and self.error_on_invalid_routes, err

            # We have a new best!
            if current_processed is False:
                assert current_ann is not None, "mypy type check"
                current_ann = self._copy_and_process(current_ann, from_rel)
                # Save to local rib
                self.local_rib.add_ann(current_ann)

        self._reset_q(reset_q)


    def _process_incoming_withdrawal(
        self: "BGPFull",
        ann: "Ann",
        from_rel: "Relationships",
    ) -> bool:
        prefix: str = ann.prefix
        neighbor: int = ann.as_path[0]
        # Return if the current ann was seeded (for an attack)
        local_rib_ann = self.local_rib.get(prefix)

        ann_info: AnnInfo | None = self.ribs_in.get_unprocessed_ann_recv_rel(
            neighbor, prefix
        )
        # ann should exist in ribs in if we are trying to withdraw it, it shouldn't be None
        assert ann_info is not None, (
            "Trying to withdraw ann that was never stored in RIBsIn "
            f"{self.as_.asn=} {self.ribs_in=} {ann=} {from_rel=}"
        ) and self.error_on_invalid_routes

        try:
            current_ann_ribs_in = ann_info.unprocessed_ann

            err = (
                f"Cannot withdraw ann that was never sent.\n\t "
                f"Ribs in: {current_ann_ribs_in}\n\t withdraw: {ann}"
            )
            assert ann.prefix_path_attributes_eq(current_ann_ribs_in) and self.error_on_invalid_routes, err

            # Remove ann from Ribs in
            self.ribs_in.remove_entry(neighbor, prefix)
        # This happens when you get a withdrawal for an announcement you never had
        # Raise if you are erroring out on this, otherwise do nothing (since it's already gone)
        except AttributeError:
            if self.error_on_invalid_routes:
                raise

        # Remove ann from local rib
        withdraw_ann: Ann = self._copy_and_process(
            ann, from_rel, overwrite_default_kwargs={"withdraw": True}
        )
        if (
            withdraw_ann.prefix_path_attributes_eq(local_rib_ann)
            and local_rib_ann.seed_asn is None
        ):
            self.local_rib.pop(prefix, None)
            # Also remove from neighbors
            self._withdraw_ann_from_neighbors(withdraw_ann)

            best_ann: Ann | None = self._select_best_ribs_in(prefix)

            # Put new ann in local rib
            if best_ann is not None:
                self.local_rib.add_ann(best_ann)

            err = "Best ann should not be identical to the one we just withdrew"
            assert not withdraw_ann.prefix_path_attributes_eq(best_ann) and self.error_on_invalid_routes, err
            return True
        return False


    def _withdraw_ann_from_neighbors(self: "BGPFull", withdraw_ann: "Ann") -> None:
        """Withdraw a route from all neighbors.

        This function will not remove an announcement from the local rib, that
        should be done before calling this function.

        Note that withdraw_ann is a deep copied ann
        """
        assert withdraw_ann.withdraw is True
        # Check ribs_out to see where the withdrawn ann was sent
        for send_neighbor in self.ribs_out.neighbors():
            # If the two announcements are equal
            if withdraw_ann.prefix_path_attributes_eq(
                self.ribs_out.get_ann(send_neighbor, withdraw_ann.prefix)
            ):
                # Delete ann from ribs out
                self.ribs_out.remove_entry(send_neighbor, withdraw_ann.prefix)
                self.send_q.add_ann(send_neighbor, withdraw_ann)

        # We may not have sent the ann yet, it may just be in the send queue
        # and not ribs out
        # We want to cancel out any anns in the send_queue that match the wdraw
        for neighbor_obj in self.as_.neighbors:
            send_info: SendInfo | None = self.send_q.get_send_info(
                neighbor_obj, withdraw_ann.prefix
            )
            if send_info is None or send_info.ann is None:
                continue
            elif send_info.ann.prefix_path_attributes_eq(withdraw_ann):
                send_info.ann = None
