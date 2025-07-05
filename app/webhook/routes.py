from flask import Blueprint, json, request, jsonify, render_template
from datetime import datetime
from app.extensions import mongo
import pytz

webhook = Blueprint('Webhook', __name__, url_prefix='/webhook')

@webhook.route('/receiver', methods=["POST"])
def receiver():
    # receiving data in form of json from webhook
    data = request.json
    # getting the event_type by headers (X-Github-Event)
    event_type = request.headers.get('X-Github-Event')

    # if we don't get the event type
    if not event_type:
        return jsonify({'error': 'Missing GitHub Event Header'}), 400

    # need modification here
    timestamp = datetime.utcnow()

    if event_type == 'push':
        author = data['pusher']['name']
        to_branch = data['ref'].split('/')[-1]
        request_id = data['after'] 
        action = 'PUSH'
        
        doc = {
            "request_id": request_id,
            "author": author,
            "action": action,
            "from_branch": "", 
            "to_branch": to_branch,
            "timestamp": timestamp,
        }

        mongo.db.events.insert_one(doc)

    elif event_type == 'pull_request':
        action_type = data['action']
        pr = data['pull_request']
        author = pr['user']['login']
        from_branch = pr['head']['ref']
        to_branch = pr['base']['ref']
        request_id = str(pr['id'])

        if action_type == 'opened':
            doc = {
                "request_id": request_id,
                "author": author,
                "action": "PULL_REQUEST",
                "from_branch": from_branch,
                "to_branch": to_branch,
                "timestamp": timestamp
            }
            mongo.db.events.insert_one(doc)
        elif action_type == 'closed' and pr.get('merged'):
            doc = {
                "request_id": request_id,
                "author": author,
                "action": "MERGE",
                "from_branch": from_branch,
                "to_branch": to_branch,
                "timestamp": timestamp
            }
            mongo.db.events.insert_one(doc)

    return ({'status': 'success'}), 200


@webhook.route('/events', methods=["GET"])
def get_events():
    events = mongo.db.events.find().sort('timestamp',-1).limit(10)
    output=[]
    for event in events:
        action = event.get('action')
        author = event.get('author')
        timestamp = event.get('timestamp').replace(tzinfo=pytz.UTC).strftime("%d %B %Y - %I:%M %p UTC")

        if action == 'PUSH':
            message = f'"{author}" pushed to "{event.get("to_branch")}" on {timestamp}'
        elif action == 'PULL_REQUEST':
            message = f'"{author}" submitted a pull request from "{event.get("from_branch")}" to "{event.get("to_branch")}" on {timestamp}'
        elif action == 'MERGE':
            message = f'"{author}" merged branch "{event.get("from_branch")}" to "{event.get("to_branch")}" on {timestamp}'
        else:
            message = 'Unknown action'

        output.append(message)

    return jsonify(output)



# endpoint for get push event
@webhook.route('/events/push', methods=["GET"])
def get_push_events():
    events = mongo.db.events.find({'action': 'PUSH'}).sort('timestamp', -1).limit(10)
    output=[]
    for event in events:
        action = event.get('action')
        author = event.get('author')
        timestamp = event.get('timestamp').replace(tzinfo=pytz.UTC).strftime("%d %B %Y - %I:%M %p UTC")

        message = f'"{author}" pushed to "{event.get("to_branch")}" on {timestamp}'

        output.append(message)

    return jsonify(output)


# endpoint for get pullrequest event
@webhook.route('/events/pullrequest', methods=["GET"])
def get_pull_request_events():
    events = mongo.db.events.find({'action': 'PULL_REQUEST'}).sort('timestamp', -1).limit(10)
    output=[]
    for event in events:
        action = event.get('action')
        author = event.get('author')
        timestamp = event.get('timestamp').replace(tzinfo=pytz.UTC).strftime("%d %B %Y - %I:%M %p UTC")

        message = f'"{author}" submitted a pull request from "{event.get("from_branch")}" to "{event.get("to_branch")}" on {timestamp}'

        output.append(message)

    return jsonify(output)


# endpoint for get merge event
@webhook.route('/events/merge', methods=["GET"])
def get_merge_events():
    events = mongo.db.events.find({'action': 'MERGE'}).sort('timestamp', -1).limit(10)
    output=[]
    for event in events:
        action = event.get('action')
        author = event.get('author')
        timestamp = event.get('timestamp').replace(tzinfo=pytz.UTC).strftime("%d %B %Y - %I:%M %p UTC")

        message = f'"{author}" merged branch "{event.get("from_branch")}" to "{event.get("to_branch")}" on {timestamp}'

        output.append(message)

    return jsonify(output)


