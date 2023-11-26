import praw


class RedditClient:
    def __init__(self, *, id, secret):
        self._reddit = praw.Reddit(
            client_id=id,
            client_secret=secret,
            user_agent="ELSEBOT",
            check_for_async=False,
        )

    def get_user_recent_post(
        self, user, *, on_subreddit: str | None = None
    ) -> praw.models.Submission | None:
        redditor: praw.models.Redditor = self._reddit.redditor(user)
        for post in redditor.submissions.new(limit=10):
            if on_subreddit:
                if post.subreddit.display_name == on_subreddit:
                    return post
            else:
                return post

    def get_post_image_count(self, url: str) -> int | None:
        post = self._reddit.submission(url=url)
        if hasattr(post, "gallery_data"):
            return len(post.gallery_data)
        if hasattr(post, "url"):
            return 1
        return None
