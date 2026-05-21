from app.celery_app import make_celery
from app import create_app
from app.models import Post
from app.services.analysis_service import AnalysisService


celery = make_celery()


def _analyze_post_impl(post_id: int):
    app = create_app()
    with app.app_context():
        post = Post.query.get(post_id)
        if not post:
            return {'error': 'Post not found'}

        service = AnalysisService()
        return service.analyze_post(post)


# Always expose analyze_post_task; if Celery is available, register as a task wrapper
if celery:
    @celery.task(name='analysis.analyze_post')
    def analyze_post_task(post_id: int):
        return _analyze_post_impl(post_id)
else:
    def analyze_post_task(post_id: int):
        return _analyze_post_impl(post_id)
