from flask import Blueprint, jsonify, request

api = Blueprint("api", __name__, url_prefix="/api/v1")

# the default todo expected by tests
DEFAULT_TODO: dict = {
    "id": 1,
    "title": "Watch CSSE6400 Lecture",
    "description": "Watch the CSSE6400 lecture on ECHO360 for week 1",
    "completed": True,
    "deadline_at": "2026-02-27T18:00:00",
    "created_at": "2026-02-20T14:00:00",
    "updated_at": "2026-02-20T14:00:00",
}

# simple in-memory store
_TODOS: dict[int, dict] = {}


def reset_store() -> None:
    """Reset in-memory store to the default state expected by tests."""
    _TODOS.clear()
    _TODOS[1] = dict(DEFAULT_TODO)


# initialise once at import time too (useful when running flask app directly)
reset_store()


@api.get("/health")
def health():
    return jsonify({"status": "ok"}), 200


@api.get("/todos")
def get_todos():
    return jsonify(list(_TODOS.values())), 200


@api.get("/todos/<int:todo_id>")
def get_todo_by_id(todo_id: int):
    todo = _TODOS.get(todo_id)
    if todo is None:
        return jsonify({"error": "not found"}), 404
    return jsonify(todo), 200


@api.post("/todos")
def post_todo():
    data = request.get_json(silent=True) or {}

    if "id" in data:
        todo_id = int(data["id"])
    else:
        todo_id = (max(_TODOS.keys()) + 1) if _TODOS else 1

    todo = dict(data)
    todo["id"] = todo_id
    _TODOS[todo_id] = todo
    return jsonify(todo), 201


@api.put("/todos/<int:todo_id>")
def put_todo(todo_id: int):
    data = request.get_json(silent=True) or {}
    todo = dict(data)
    todo["id"] = todo_id
    _TODOS[todo_id] = todo
    return jsonify(todo), 200


@api.delete("/todos/<int:todo_id>")
def delete_todo(todo_id: int):
    todo = _TODOS.pop(todo_id, None)
    if todo is None:
        return jsonify({"error": "not found"}), 404
    return jsonify(todo), 200