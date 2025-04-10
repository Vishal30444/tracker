from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, logout_user, current_user
from models import User, Project, db
from app import app, login_manager
import time
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        role = 'normal'  # Default role for new users

        if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
            flash('Username or Email already exists!')
            return redirect(url_for('login'))
        
        new_user = User(name=name, email=email, username=username, role=role, password=password)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash('Signup request submitted. Please wait for approval.')
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            if not user.approved:
                flash('Your account is pending approval.')
                return redirect(url_for('login'))
            login_user(user)
            return redirect(url_for('home') if user.role == 'normal' else url_for('view_projects'))
        flash('Invalid credentials!')
    return render_template('login.html')

@app.route('/approve-users', methods=['GET', 'POST'])
@login_required
def approve_users():
    if current_user.role == 'supervisor' or current_user.role == 'manager':
        users = User.query.filter_by(approved=False).all()
        if request.method == 'POST':
            user_id = request.form.get('user_id')
            action = request.form.get('action')
            user = User.query.get(user_id)
            
            if action == 'approve':
                user.approved = True
            elif action == 'reject':
                db.session.delete(user)
            
            db.session.commit()
            flash('User approval updated!')
            return redirect(url_for('approve_users'))
        
        return render_template('approve_users.html', users=users)
    else:
        return redirect(url_for('home'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Home page: project submission
@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    if current_user.role == 'normal':
        print("normal lllll")
        if request.method == 'POST':
            print("post")
            thematic_area = request.form.get('thematic_area')
            project_title = request.form.get('project_title')
            continent = request.form.get('continent')
            country = request.form.get('country')
            if country == "others":
                print("others")
                country = request.form.get('country_other')
            city_state = request.form.get('city_state')
            funding_agency = request.form.get('funding_agency')
            if funding_agency == "others":
                funding_agency = request.form.get('funding_agency_other')
            final_funder = request.form.get('final_funder')
            type_of_procurement = request.form.get('type_of_procurement')
            if type_of_procurement == "others":
                type_of_procurement = request.form.get('type_of_procurement_other')

            budget = request.form.get('budget')
            currency_type=request.form.get('currency_type')
            opportunity_published_date = request.form.get('opportunity_published_date')
            deadline = request.form.get('deadline')
            project_duration = request.form.get('project_duration')
            key_expert = request.form.get('key_expert')
            non_key_expert = request.form.get('non_key_expert')
            proposed_contract_type = request.form.get('proposed_contract_type')
            objectives = request.form.get('objectives')
            links = request.form.get('links')
            comments = request.form.get('comments')

            # Validate required fields
            if not (thematic_area and project_title):
                print("no post")
                flash('All fields are required.', 'error')
            else:
                print("post")
                project = Project(
                    thematic_area=thematic_area,
                    project_title=project_title,
                    continent=continent,
                    country=country,
                    city_state=city_state,
                    funding_agency=funding_agency,
                    final_funder=final_funder,
                    type_of_procurement=type_of_procurement,
                    budget=budget,
                    currency_type = currency_type,
                    opportunity_published_date=opportunity_published_date,
                    deadline=deadline,
                    project_duration=project_duration,
                    key_expert=key_expert,
                    non_key_expert=non_key_expert,
                    proposed_contract_type=proposed_contract_type,
                    objectives=objectives,
                    links=links,
                    comments=comments,
                    created_by=current_user.id
                )
                db.session.add(project)
                db.session.commit()
                flash('Project submitted successfully.', 'success')
                time.sleep(3)
                return redirect(url_for('success'))

        return render_template('home.html')
    else:
        return redirect(url_for('view_projects'))


# View projects page
@app.route('/view', methods=['GET', 'POST'])
@login_required
def view_projects():
    # Get projects based on user role
    if current_user.role == 'normal':
        projects = Project.query.filter_by(created_by=current_user.id).all()
    else:
        projects = Project.query.all()

    # Fetch all users and create a dictionary {user_id: user_name}
    users = {user.id: user.name for user in User.query.all()}
    # Get unique submitter names from current projects
    unique_submitters = sorted(
        {users[project.created_by] for project in projects if project.created_by in users},
        key=lambda x: x.lower()  # Case-insensitive sorting
    )

    unique_funding_agencies = sorted(
        {project.funding_agency for project in projects if project.funding_agency},
        key=lambda x: x.lower()
    )

    # Handle approval actions if form submitted
    if request.method == 'POST':
        project_id = request.form.get('project_id')
        action = request.form.get('action')
        comments = request.form.get('comments')
        project = Project.query.get(project_id)
        
        if project:
            if current_user.role == 'manager':
                project.manager_status = 'Approved' if action == 'approve' else 'Rejected'
                project.manager_comments = comments
            elif current_user.role == 'supervisor':
                project.supervisor_status = 'Approved' if action == 'approve' else 'Rejected'
                project.supervisor_comments = comments
            
            db.session.commit()
            flash('Project status updated successfully.')
            return redirect(url_for('view_projects'))

    return render_template(
        'view.html',
        projects=projects,
        users=users,
        user_role=current_user.role,
        unique_submitters=unique_submitters,
        unique_funding_agencies=unique_funding_agencies
    )

@app.route('/success')
@login_required
def success():
    return render_template('success.html')

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.role not in ['manager', 'supervisor']:
        flash("Access Denied.")
        return redirect(url_for('home'))

    # Get filters from query parameters
    username = request.args.get('username')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    # Start with all projects
    query = Project.query

    # Filter by username (join with User table)
    if username:
        query = query.join(User).filter(User.name == username)

    # Filter by date range
    if start_date:
        query = query.filter(Project.created_on >= start_date)
    if end_date:
        query = query.filter(Project.created_on <= end_date)

    # Apply filtered query to count data
    filtered_projects = query.all()

    # Compute counts based on filtered data
    total_projects = len(filtered_projects)
    manager_pending = sum(1 for p in filtered_projects if p.manager_status == 'Pending')
    supervisor_pending = sum(1 for p in filtered_projects if p.supervisor_status == 'Pending')
    manager_approved = sum(1 for p in filtered_projects if p.manager_status == 'Approved')
    manager_rejected = sum(1 for p in filtered_projects if p.manager_status == 'Rejected')
    supervisor_approved = sum(1 for p in filtered_projects if p.supervisor_status == 'Approved')
    supervisor_rejected = sum(1 for p in filtered_projects if p.supervisor_status == 'Rejected')

    # For dropdown: unique user names (if not passed already)
    all_users = User.query.all()
    unique_submitters = list(set(user.name for user in all_users))

    data = {
        'total_projects': total_projects,
        'manager_pending': manager_pending,
        'supervisor_pending': supervisor_pending,
        'manager_approved': manager_approved,
        'manager_rejected': manager_rejected,
        'supervisor_approved': supervisor_approved,
        'supervisor_rejected': supervisor_rejected,
    }

    return render_template('dashboard.html', data=data, unique_submitters=unique_submitters)

# @app.route('/dashboard')
# @login_required
# def dashboard():
#     if current_user.role not in ['manager', 'supervisor']:
#         flash("Access Denied.")
#         return redirect(url_for('home'))

#     # Total projects submitted
#     total_projects = Project.query.count()
  
#     # # Projects submitted within a date range (if provided as query parameters)
#     # # Expecting start_date and end_date in 'YYYY-MM-DD' format
#     # start_date = request.args.get('start_date')
#     # end_date = request.args.get('end_date')
#     # projects_in_range = None
#     # if start_date and end_date:
#     #     projects_in_range = Project.query.filter(
#     #         Project.created_on.between(start_date, end_date)
#     #     ).count()

#     # Pending approvals from manager and supervisor
#     manager_pending = Project.query.filter_by(manager_status='Pending').count()
#     supervisor_pending = Project.query.filter_by(supervisor_status='Pending').count()

#     # Approved and rejected counts (from manager and supervisor)
#     manager_approved = Project.query.filter_by(manager_status='Approved').count()
#     manager_rejected = Project.query.filter_by(manager_status='Rejected').count()
#     supervisor_approved = Project.query.filter_by(supervisor_status='Approved').count()
#     supervisor_rejected = Project.query.filter_by(supervisor_status='Rejected').count()

#     data = {
#         'total_projects': total_projects,
#         # 'projects_in_range': projects_in_range,
#         'manager_pending': manager_pending,
#         'supervisor_pending': supervisor_pending,
#         'manager_approved': manager_approved,
#         'manager_rejected': manager_rejected,
#         'supervisor_approved': supervisor_approved,
#         'supervisor_rejected': supervisor_rejected,
#     }

#     return render_template('dashboard.html', data=data)


@app.route("/userprofile")
@login_required
def view_all_users():
    if current_user.role != 'supervisor':
        return redirect(url_for('home'))
    users=User.query.all()
    return render_template('userprofile.html',users=users)