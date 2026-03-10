from flask import Flask, render_template, request, redirect
from db_config import get_db_connection
import json
import difflib

app = Flask(__name__)

@app.route("/")
def dashboard():

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM workflows")
    workflows = cur.fetchall()

    conn.close()

    return render_template("dashboard.html", workflows=workflows)

@app.route("/create")
def create_page():
    return render_template("create_workflow.html")

#to create new workflow
@app.route("/create-workflow", methods=["POST"])
def create_workflow():

    name = request.form["name"]
    description = request.form["description"]
    stages = request.form.getlist("stages")

    config = json.dumps({"stages": stages})

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO workflows (name,description) VALUES (%s,%s)",
        (name, description)
    )

    workflow_id = cur.lastrowid

    cur.execute(
        """INSERT INTO workflow_versions
        (workflow_id,version_number,configuration)
        VALUES (%s,%s,%s)""",
        (workflow_id,1,config)
    )

    conn.commit()
    conn.close()

    return redirect("/")

@app.route("/edit/<int:id>")
def edit_workflow(id):

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM workflows WHERE id=%s",(id,))
    workflow = cur.fetchone()

    conn.close()

    return render_template("edit_workflow.html", workflow=workflow)

@app.route("/update/<int:id>", methods=["POST"])
def update_workflow(id):

    stages = request.form.getlist("stages")

    config = json.dumps({"stages": stages})

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT current_version FROM workflows WHERE id=%s",
        (id,)
    )

    version = cur.fetchone()[0] + 1

    cur.execute(
        """INSERT INTO workflow_versions
        (workflow_id,version_number,configuration)
        VALUES (%s,%s,%s)""",
        (id,version,config)
    )

    cur.execute(
        "UPDATE workflows SET current_version=%s WHERE id=%s",
        (version,id)
    )

    conn.commit()
    conn.close()

    return redirect("/")

#to delete exissting workflow
@app.route("/delete/<int:id>")
def delete_workflow(id):

    conn = get_db_connection()
    cur = conn.cursor()

    # delete versions first
    cur.execute(
        "DELETE FROM workflow_versions WHERE workflow_id=%s",
        (id,)
    )

    # delete workflow
    cur.execute(
        "DELETE FROM workflows WHERE id=%s",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/")

#to view the history
@app.route('/history/<int:workflow_id>')
def history(workflow_id):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT version_number, configuration, created_at
        FROM workflow_versions
        WHERE workflow_id = %s
        ORDER BY version_number
    """, (workflow_id,))

    rows = cursor.fetchall()

    versions = []
    for r in rows:
        config = json.loads(r[1])
        stages = ", ".join(config["stages"])

        versions.append({
            "version": r[0],
            "stages": stages,
            "date": r[2]
        })

    cursor.close()
    conn.close()

    return render_template("history.html", versions=versions, workflow_id=workflow_id)

#to compare the versions
@app.route("/compare/<int:id>", methods=["POST"])
def compare_versions(id):

    v1 = request.form.get("version1")
    v2 = request.form.get("version2")

    if not v1 or not v2:
        return "Please select 2 versions to compare."

    if v1 == v2:
        return "Please select two different versions."

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT configuration FROM workflow_versions WHERE workflow_id=%s AND version_number=%s",
        (id, v1)
    )
    config1 = json.loads(cur.fetchone()[0])

    cur.execute(
        "SELECT configuration FROM workflow_versions WHERE workflow_id=%s AND version_number=%s",
        (id, v2)
    )
    config2 = json.loads(cur.fetchone()[0])

    conn.close()

    diff = list(difflib.ndiff(config1["stages"], config2["stages"]))

    return render_template("compare.html", diff=diff)

if __name__ == "__main__":
    app.run(debug=True)