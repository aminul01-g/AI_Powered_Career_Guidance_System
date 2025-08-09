from flask import Blueprint, request, jsonify, current_app, send_from_directory
from extensions import db
from models import GuidanceSession, Upload, User
from flask_jwt_extended import jwt_required, get_jwt_identity
import os, uuid, json, requests

guidance_bp = Blueprint('guidance', __name__)

@guidance_bp.route('/upload_resume', methods=['POST'])
@jwt_required(optional=True)
def upload_resume():
    uid = get_jwt_identity()
    if 'file' not in request.files:
        return jsonify({'error': 'no file provided'}), 400
    f = request.files['file']
    filename = f.filename
    os.makedirs(current_app.config['UPLOAD_FOLDER'], exist_ok=True)
    unique_name = f"{uuid.uuid4().hex}_{filename}"
    path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_name)
    f.save(path)
    up = Upload(user_id=uid, filename=filename, filepath=path)
    db.session.add(up)
    db.session.commit()
    return jsonify({'upload_id': up.id, 'filename': filename})

@guidance_bp.route('/uploads/<int:upload_id>', methods=['GET'])
def download_upload(upload_id):
    up = Upload.query.get(upload_id)
    if not up:
        return jsonify({'error':'not found'}), 404
    directory = os.path.dirname(up.filepath)
    return send_from_directory(directory, os.path.basename(up.filepath), as_attachment=True)

@guidance_bp.route('/ai/recommend', methods=['POST'])
@jwt_required(optional=True)
def ai_recommend():
    data = request.json or {}
    profile = data.get('profile') or {}
    goals = data.get('goals') or ''
    # simple placeholder: call OpenAI if key present, otherwise return mock
    key = os.getenv('OPENAI_API_KEY') or current_app.config.get('OPENAI_API_KEY')
    prompt = f"Make a short career recommendation for goals: {goals} and profile: {profile}"
    result = {'recommendation': 'mock suggestion: build projects, learn data structures, apply to internships'}
    if key:
        try:
            import requests, os, json
            headers = {'Authorization': f'Bearer {key}', 'Content-Type':'application/json'}
            # This is a placeholder. The real api call depends on the model/provider.
            payload = { 'model': 'gpt-4o-mini', 'input': prompt }
            resp = requests.post('https://api.openai.com/v1/responses', headers=headers, json=payload, timeout=15)
            if resp.status_code == 200:
                j = resp.json()
                result['recommendation'] = j.get('output') or j
            else:
                result['api_error'] = resp.text
        except Exception as e:
            result['error'] = str(e)
    # save session
    gs = GuidanceSession(user_id=get_jwt_identity(), inputs_json=json.dumps({'profile':profile,'goals':goals}), result_json=json.dumps(result))
    db.session.add(gs)
    db.session.commit()
    return jsonify({'session_id': gs.id, 'result': result})

@guidance_bp.route('/analytics/event', methods=['POST'])
def analytics_event():
    data = request.json or {}
    name = data.get('name')
    metadata = data.get('metadata', {})  # kept name 'metadata' as local variable
    uid = get_jwt_identity() if hasattr(request, 'jwt_identity') else None
    from models import Event
    ev = Event(user_id=uid, name=name, metadata_json=json.dumps(metadata))
    db.session.add(ev)
    db.session.commit()
    return jsonify({'status':'ok', 'event_id': ev.id})
