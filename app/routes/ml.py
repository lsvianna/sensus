from flask import request, jsonify
from app.routes import api_bp
from app.models import db, MLExperiment
from app.utils.time import utcnow


@api_bp.route('/ml/experiments', methods=['GET'])
def list_experiments():
    experiments = MLExperiment.query.order_by(MLExperiment.created_at.desc()).all()
    return jsonify({
        'experiments': [
            {
                'id': e.id,
                'name': e.name,
                'description': e.description,
                'params': e.params,
                'metrics': e.metrics,
                'status': e.status,
                'created_at': e.created_at.isoformat()
            } for e in experiments
        ]
    }), 200


@api_bp.route('/ml/train', methods=['POST'])
def create_experiment():
    data = request.get_json() or {}
    name = data.get('name', f"run-{int(utcnow().timestamp())}")
    exp = MLExperiment(
        name=name,
        description=data.get('description', ''),
        params=data.get('params', {}),
        metrics={},
        status='running'
    )
    db.session.add(exp)
    db.session.commit()

    # Placeholder: in a real setup we'd enqueue a training task
    exp.status = 'completed'
    exp.metrics = {'dummy_accuracy': 0.5}
    db.session.add(exp)
    db.session.commit()

    return jsonify({'experiment_id': exp.id, 'status': exp.status}), 201
