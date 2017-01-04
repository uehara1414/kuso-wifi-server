from django.test import TestCase
from django.utils import timezone

from .models import WifiReport
from .twitter import create_tweet_content


class TweetTest(TestCase):

    def test_create_tweet_comment_1(self):
        report_with_comment = WifiReport.create_new("test-uid", "test-wifi", timezone.now(), 100, "Hello Comment", do_tweet=False)
        self.assertEqual(
            create_tweet_content(report_with_comment),
            "{}:{} に test-wifi に対して以下の苦言が呈されました。\n"
            "「Hello Comment」\n"
            "ping: 100\n"
            "#kuso-wifi-button".format(report_with_comment.date.hour, report_with_comment.date.minute))

    def test_create_tweet_comment_2(self):
        # Too long comment
        report_with_comment = WifiReport.create_new("test-uid", "test-wifi", timezone.now(), 100, "long" * 100, do_tweet=False)
        self.assertEqual(create_tweet_content(report_with_comment), "")
