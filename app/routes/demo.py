from datetime import timedelta

from flask import jsonify
from werkzeug.security import generate_password_hash

from app.models import Analysis, Comment, InstagramAccount, Post, User, db
from app.routes import api_bp
from app.utils.time import utcnow


@api_bp.route("/demo/seed", methods=["POST"])
def seed_demo_data():
    """Create deterministic local demo data for manual testing."""

    user = User.query.filter_by(email="demo@sensus.local").first()
    if not user:
        user = User(
            email="demo@sensus.local",
            username="demo",
            full_name="Demo Sensus",
            password_hash=generate_password_hash("demo123"),
        )
        db.session.add(user)
        db.session.flush()

    account = InstagramAccount.query.filter_by(user_id=user.id, username="sensus_demo").first()
    if not account:
        account = InstagramAccount(
            user_id=user.id,
            instagram_id=f"local_{user.id}_sensus_demo",
            username="sensus_demo",
            display_name="Sensus Demo",
            bio="Conta local para validar o dashboard.",
            followers_count=12840,
            following_count=420,
            last_sync=utcnow(),
        )
        db.session.add(account)
        db.session.flush()

    samples = [
        ("Campanha nova gerando respostas muito boas do publico.", 820, 96, 6.4, "positive", 0.72),
        ("Post educativo com bastante salvamento e comentarios neutros.", 410, 38, 3.2, "neutral", 0.08),
        ("Feedback misto sobre mudancas recentes no produto.", 260, 44, 2.1, "negative", -0.34),
    ]

    for index, sample in enumerate(samples, start=1):
        caption, likes, comments_count, engagement, label, score = sample
        instagram_id = f"demo_post_{account.id}_{index}"
        post = Post.query.filter_by(instagram_id=instagram_id).first()
        if not post:
            post = Post(
                account_id=account.id,
                instagram_id=instagram_id,
                caption=caption,
                media_type="IMAGE",
                likes_count=likes,
                comments_count=comments_count,
                engagement_rate=engagement,
                sentiment_label=label,
                sentiment_score=score,
                posted_at=utcnow() - timedelta(days=index),
            )
            db.session.add(post)
            db.session.flush()

            for comment_index in range(1, 4):
                db.session.add(Comment(
                    post_id=post.id,
                    instagram_id=f"demo_comment_{post.id}_{comment_index}",
                    author_username=f"cliente_{comment_index}",
                    text="Comentario de exemplo para validar a analise local.",
                    likes_count=comment_index,
                    sentiment_label=label,
                    sentiment_score=score,
                    created_at=utcnow() - timedelta(days=index, minutes=comment_index),
                ))

            db.session.add(Analysis(
                post_id=post.id,
                total_comments=comments_count,
                positive_comments=comments_count if label == "positive" else 6,
                negative_comments=comments_count if label == "negative" else 4,
                neutral_comments=comments_count if label == "neutral" else 10,
                average_sentiment=score,
                engagement_trend="rising" if label == "positive" else "stable",
                hashtags=["sensus", "analytics", "demo"],
                mentions=["sensus_demo"],
                top_keywords=["engajamento", "publico", "conteudo"],
            ))

    db.session.commit()

    return jsonify({
        "message": "Demo data ready",
        "email": "demo@sensus.local",
        "password": "demo123",
        "user_id": user.id,
        "account_id": account.id,
    }), 201

