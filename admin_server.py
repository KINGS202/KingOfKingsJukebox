from flask import Flask, request, jsonify, send_file
import os, json, time
import jwt
app = Flask('king_admin')
CFG = {}
cfg_path = os.path.join('config','settings.json')
if os.path.exists(cfg_path):
    CFG = json.load(open(cfg_path))
JWT_SECRET = CFG.get('jwt_secret','REPLACE_THIS_SECRET')

# helper to require token
def require_jwt(f):
    def wrapper(*args, **kwargs):
        auth = request.headers.get('Authorization','')
        if not auth.startswith('Bearer '):
            return jsonify({'error':'auth required'}),401
        token = auth.split(' ',1)[1]
        try:
            data = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        except Exception:
            return jsonify({'error':'invalid token'}),401
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper
@app.route('/api/status')
def status():
    return jsonify({'ok':True,'version':CFG.get('version','unknown'),'theme':CFG.get('theme','king_modern')})
@app.route('/api/theme', methods=['POST'])
def set_theme():
    data = request.json or {}
    theme = data.get('theme')
    if theme:
        CFG['theme'] = theme
        with open(cfg_path,'w') as f: json.dump(CFG,f,indent=2)
        return jsonify({'ok':True,'theme':theme})
    return jsonify({'error':'no theme supplied'}),400

@app.route('/admin')
def admin_page():
    return send_file('server/static/admin_app/react/index.html')

if __name__=='__main__':
    app.run(host='0.0.0.0', port=5000)



from flask import request, send_from_directory
import jwt, time
JWT_SECRET = 'REPLACE_THIS_SECRET'

@app.route('/token', methods=['POST'])
def token():
    data = request.json or {}
    if data.get('admin_key') == 'supersecret':
        payload = {'admin':True,'iat':int(time.time())}
        token = jwt.encode(payload, JWT_SECRET, algorithm='HS256')
        return jsonify({'token':token})
    return jsonify({'error':'invalid'}),401

@app.route('/admin_app')
def admin_app():
    # Serve React admin SPA
    return send_from_directory('server/static/admin_app/react', 'index.html')


@app.route('/api/queue', methods=['GET','POST'])
def api_queue():
    qfile = os.path.join('data','queue.json')
    if request.method == 'GET':
        if os.path.exists(qfile):
            return jsonify(json.load(open(qfile)))
        return jsonify([])
    else:
        data = request.json or {}
        song = data.get('song') or data.get('path')
        if not song:
            return jsonify({'error':'no song'}),400
        os.makedirs('data', exist_ok=True)
        q = []
        if os.path.exists(qfile):
            q = json.load(open(qfile))
        q.append(song)
        json.dump(q, open(qfile,'w'), indent=2)
        return jsonify({'ok':True,'queue':q})

@app.route('/api/play', methods=['POST'])
@require_jwt
def api_play():
    data = request.json or {}
    path = data.get('path')
    if not path or not os.path.exists(path):
        return jsonify({'error':'invalid path'}),400
    # write to queue and return ok
    qfile = os.path.join('data','queue.json')
    os.makedirs('data', exist_ok=True)
    q = []
    if os.path.exists(qfile):
        q = json.load(open(qfile))
    q.insert(0, path)  # play next
    json.dump(q, open(qfile,'w'), indent=2)
    return jsonify({'ok':True})

@app.route('/api/volume', methods=['POST'])
@require_jwt
def api_volume():
    data = request.json or {}
    vol = int(data.get('volume',80))
    # save to config for app to pick up on next loop or via polling
    CFG['volume'] = vol
    with open(cfg_path,'w') as f: json.dump(CFG,f,indent=2)
    return jsonify({'ok':True,'volume':vol})

@app.route('/token', methods=['POST'])
def token():
    data = request.json or {}
    if data.get('admin_key') == 'supersecret':
        payload = {'admin':True,'iat':int(time.time())}
        token = jwt.encode(payload, JWT_SECRET, algorithm='HS256')
        return jsonify({'token':token})
    return jsonify({'error':'invalid'}),401
