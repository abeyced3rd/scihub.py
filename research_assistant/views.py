import os
import uuid
from flask import Blueprint, request, jsonify, current_app, send_file, abort
from . import db
from .models import Material, Chapter, Section
from .utils import extract_text_from_pdf

bp = Blueprint('ra', __name__, url_prefix='/ra', template_folder='templates')


@bp.route('/materials', methods=['POST'])
def upload_material():
    f = request.files.get('file')
    if not f:
        return jsonify({'error': 'file required'}), 400
    filename = f.filename
    uid = str(uuid.uuid4())
    storage_dir = current_app.config.get('UPLOAD_FOLDER', 'downloads')
    os.makedirs(storage_dir, exist_ok=True)
    path = os.path.join(storage_dir, f"{uid}_{filename}")
    f.save(path)
    text = ''
    if filename.lower().endswith('.pdf'):
        text = extract_text_from_pdf(path)
    m = Material(filename=filename, file_path=path, extracted_text=text)
    db.session.add(m)
    db.session.commit()
    return jsonify({'id': m.id, 'filename': filename})


@bp.route('/materials', methods=['GET'])
def list_materials():
    mats = Material.query.order_by(Material.uploaded_at.desc()).all()
    out = []
    for m in mats:
        out.append({'id': m.id, 'filename': m.filename, 'uploaded_at': m.uploaded_at.isoformat()})
    return jsonify(out)


@bp.route('/materials/<int:mid>', methods=['GET'])
def get_material(mid):
    m = Material.query.get_or_404(mid)
    chapters = []
    for ch in sorted(m.chapters, key=lambda x: x.order):
        chapters.append({'id': ch.id, 'title': ch.title, 'description': ch.description})
    return jsonify({'id': m.id, 'filename': m.filename, 'uploaded_at': m.uploaded_at.isoformat(), 'chapters': chapters})


@bp.route('/chapters/<int:cid>/sections', methods=['POST'])
def create_section(cid):
    ch = Chapter.query.get_or_404(cid)
    data = request.get_json() or {}
    title = data.get('title') or 'Untitled Section'
    content = data.get('content', '')
    order = data.get('order', 0)
    s = Section(title=title, content=content, chapter=ch, order=order)
    db.session.add(s)
    db.session.commit()
    return jsonify({'id': s.id, 'title': s.title})


@bp.route('/sections/<int:sid>', methods=['PATCH'])
def update_section(sid):
    s = Section.query.get_or_404(sid)
    data = request.get_json() or {}
    if 'title' in data:
        s.title = data.get('title')
    if 'content' in data:
        s.content = data.get('content')
    if 'order' in data:
        s.order = data.get('order')
    db.session.commit()
    return jsonify({'id': s.id, 'title': s.title})


@bp.route('/materials/<int:mid>/chapters', methods=['POST'])
def create_chapter(mid):
    m = Material.query.get_or_404(mid)
    data = request.get_json() or {}
    title = data.get('title') or 'Untitled Chapter'
    desc = data.get('description', '')
    ch = Chapter(title=title, description=desc, material=m)
    db.session.add(ch)
    db.session.commit()
    return jsonify({'id': ch.id, 'title': ch.title})


@bp.route('/chapters/<int:cid>/generate-sections', methods=['POST'])
def generate_sections(cid):
    ch = Chapter.query.get_or_404(cid)
    text = ch.material.extracted_text or ''
    if not text:
        return jsonify({'error': 'No text available in material to generate sections'}), 400
    # simple heuristic: split by double newline into paragraphs (limit to 10)
    parts = [p.strip() for p in text.split('\n\n') if p.strip()][:10]
    # clear existing
    Section.query.filter_by(chapter_id=ch.id).delete()
    sections = []
    for i, p in enumerate(parts, 1):
        s = Section(title=f'Section {i}', content=p, chapter=ch, order=i)
        db.session.add(s)
        sections.append({'title': s.title, 'content': s.content})
    db.session.commit()
    return jsonify({'success': True, 'sections': sections})


@bp.route('/chapters/<int:cid>/sections', methods=['GET'])
def list_sections(cid):
    ch = Chapter.query.get_or_404(cid)
    out = []
    for s in sorted(ch.sections, key=lambda x: x.order):
        out.append({'id': s.id, 'title': s.title, 'order': s.order})
    return jsonify(out)


@bp.route('/sections/<int:sid>', methods=['GET'])
def get_section(sid):
    s = Section.query.get_or_404(sid)
    return jsonify({'id': s.id, 'title': s.title, 'content': s.content, 'order': s.order})
