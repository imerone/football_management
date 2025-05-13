from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from forms import TeamForm
from blueprints.auth import login_required

team_bp = Blueprint('team', __name__)

@team_bp.route('/dashboard')
@login_required
def dashboard():
    from models import Team, db
    teams = Team.query.filter_by(user_id=session['user_id']).all()
    return render_template('team/dashboard.html', teams=teams)

@team_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    from models import Team, db
    form = TeamForm()
    if form.validate_on_submit():
        team = Team(
            name=form.name.data,
            coach=form.coach.data,
            founded_year=form.founded_year.data,
            user_id=session['user_id']
        )
        db.session.add(team)
        db.session.commit()
        flash('Team created successfully!', 'success')
        return redirect(url_for('team.dashboard'))
    return render_template('team/create.html', form=form)

@team_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    from models import Team, db
    team = Team.query.get_or_404(id)
    if team.user_id != session['user_id']:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('team.dashboard'))
    form = TeamForm(obj=team)
    if form.validate_on_submit():
        team.name = form.name.data
        team.coach = form.coach.data
        team.founded_year = form.founded_year.data
        db.session.commit()
        flash('Team updated successfully!', 'success')
        return redirect(url_for('team.dashboard'))
    return render_template('team/edit.html', form=form, team=team)

@team_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    from models import Team, db
    team = Team.query.get_or_404(id)
    if team.user_id != session['user_id']:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('team.dashboard'))
    db.session.delete(team)
    db.session.commit()
    flash('Team deleted successfully!', 'success')
    return redirect(url_for('team.dashboard'))
