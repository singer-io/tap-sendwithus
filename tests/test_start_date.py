from datetime import datetime, timedelta, timezone

from base import SendwithusBaseTest
from tap_tester import LOGGER, connections, runner
from tap_tester.base_suite_tests.start_date_test import StartDateTest


class SendwithusStartDateTest(StartDateTest, SendwithusBaseTest):
    """Instantiate start date according to the desired data set and run the
    test."""

    # Note: Start date test may fail for logs and log_events as the sendwithus
    # Account has 7 day data retention policy (free version).
    # User may need to regenerate data within the retention period to have
    # consistent test results using `generate-logs-data.py` present in spikes.
    # Also create new templates and snippets with created/modified date after
    # start_date_2 to have data for both syncs.

    # Steps to Ensure Consistent Test Results:
    # 1. Use the script to generate logs and log_events data.
    # 2. Generate data 2 times with a gap of few mins between them to have consistent test results as start_date_2 is having a delta of 5 mins.
    # 3. Create new templates and snippets with created/modified date after start_date_2.

    _bookmark_format = "%Y-%m-%dT%H:%M:%S.%fZ"
    # Streams whose max bookmark from sync 1 drives start_date_2
    _lookback_streams = {"logs": "created"}
    _lookback_delta = timedelta(minutes=0)
    # Populated dynamically between syncs
    _computed_start_date_2 = None

    @staticmethod
    def name():
        return "tap_tester_sendwithus_start_date_test"

    def streams_to_test(self):
        # Excluding drip_campaigns since it uses full table replication
        streams_to_exclude = {"drip_campaigns", "log_events"}
        return self.expected_stream_names().difference(streams_to_exclude)

    @property
    def start_date_1(self):
        return "2015-03-25T00:00:00.000000Z"

    @property
    def start_date_2(self):
        """Returns the max bookmark of logs/log_events from sync 1 minus 30
        minutes. Falls back to now - 30 minutes if sync 1 has not yet run."""
        if self.__class__._computed_start_date_2:
            return self.__class__._computed_start_date_2
        return (
            datetime.now(tz=timezone.utc) - self.__class__._lookback_delta
        ).strftime(self.__class__._bookmark_format)

    def _compute_start_date_2_from_sync1(self):
        """Derives start_date_2 from the max replication key value across
        logs and log_events in sync 1 results, minus the lookback delta."""
        max_bookmark = None
        for stream, rep_key in self.__class__._lookback_streams.items():
            messages = (
                StartDateTest.synced_messages_by_stream_1
                .get(stream, {})
                .get('messages', [])
            )
            for msg in messages:
                if msg.get('action') != 'upsert':
                    continue
                raw = msg['data'].get(rep_key)
                if not raw:
                    continue
                parsed = datetime.strptime(
                    raw, self.__class__._bookmark_format
                ).replace(tzinfo=timezone.utc)
                if max_bookmark is None or parsed > max_bookmark:
                    max_bookmark = parsed
        if max_bookmark:
            self.__class__._computed_start_date_2 = (
                max_bookmark - self.__class__._lookback_delta
            ).strftime(self.__class__._bookmark_format)

    def setUp(self):  # pylint: disable=invalid-name
        """
        Note: We are overriding the base class to get the ability to compute start_date_2 from sync 1 results.
        Reason being the account data is dynamic and we want to be able to compute start_date_2 based on the actual data synced in sync 1 to have consistent test results.

        Method: _compute_start_date_2_from_sync1
            Gets the max_bookmark from logs are sets it to start_date_2 with a lookback delta subtracted from it. This ensures that we have data for both sync 1 and sync 2 and the test results are consistent.
        """
        cached_variables = all([
            StartDateTest.record_count_by_stream_1,
            StartDateTest.synced_messages_by_stream_1,
            StartDateTest.record_count_by_stream_2,
            StartDateTest.synced_messages_by_stream_2])

        if not cached_variables:
            self.assertGreater(self.start_date_2, self.start_date_1)

            ##########################################################################
            # First Sync
            ##########################################################################

            # instantiate connection
            self.start_date = self.start_date_1
            conn_id_1 = connections.ensure_connection(self)

            # run check mode
            found_catalogs_1 = self.run_and_verify_check_mode(conn_id_1)

            # table and field selection
            test_catalogs_1 = [catalog for catalog in found_catalogs_1
                               if catalog.get('stream_name') in self.streams_to_test()]

            # non_selected_fields are none
            self.perform_and_verify_table_and_field_selection(conn_id_1, test_catalogs_1)

            # run initial sync
            StartDateTest.record_count_by_stream_1 = self.run_and_verify_sync_mode(conn_id_1)
            StartDateTest.synced_messages_by_stream_1 = runner.get_records_from_target_output()

            ##########################################################################
            # Compute start_date_2 from sync 1 max bookmark - delta min
            ##########################################################################

            self._compute_start_date_2_from_sync1()

            LOGGER.info(
                "REPLICATION START DATE CHANGE: %s ===>>> %s",
                self.start_date_1, self.start_date_2
            )
            self.assertGreater(self.start_date_2, self.start_date_1)
            self.start_date = self.start_date_2

            ##########################################################################
            # Second Sync
            ##########################################################################

            # create a new connection with the new start_date
            conn_id_2 = connections.ensure_connection(self)

            # run check mode
            found_catalogs_2 = self.run_and_verify_check_mode(conn_id_2)

            # table and field selection
            test_catalogs_2 = [catalog for catalog in found_catalogs_2
                               if catalog.get('stream_name') in self.streams_to_test()]

            # non_selected_fields are none
            self.perform_and_verify_table_and_field_selection(conn_id_2, test_catalogs_2)

            # run second sync
            StartDateTest.record_count_by_stream_2 = self.run_and_verify_sync_mode(conn_id_2)
            StartDateTest.synced_messages_by_stream_2 = runner.get_records_from_target_output()
