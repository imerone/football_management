from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import Match, Team, db
from forms import MatchForm, SearchForm
from blueprints.auth import login_required

match_bp = Blueprint('match', __name__)

@match_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = MatchForm()
    teams = Team.query.filter_by(user_id=session['user_id']).all()
    form.team1_id.choices = [(team.id, team.name) for team in teams]
    form.team2_id.choices = [(team.id, team.name) for team in teams]
    if form.validate_on_submit():
        if form.team1_id.data == form.team2_id.data:
            flash('Teams cannot play against themselves.', 'danger')
            return render_template('match/create.html', form=form, teams=teams)
        match = Match(
            team1_id=form.team1_id.data,
            team2_id=form.team2_id.data,
            score=form.score.data,
            date=form.date.data
        )
        db.session.add(match)
        db.session.commit()
        flash('Match created successfully!', 'success')
        return redirect(url_for('match.list'))
    return render_template('match/create.html', form=form, teams=teams)

@match_bp.route('/list')
@login_required
def list():
    matches = Match.query.join(Team, Match.team1_id == Team.id).filter(Team.user_id == session['user_id']).all()
    return render_template('match/list.html', matches=matches)

@match_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    match = Match.query.get_or_404(id)
    if match.team1.user_id != session['user_id']:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('match.list'))
    form = MatchForm(obj=match)
    teams = Team.query.filter_by(user_id=session['user_id']).all()
    form.team1_id.choices = [(team.id, team.name) for team in teams]
    form.team2_id.choices = [(team.id, team.name) for team in teams]
    if form.validate_on_submit():
        if form.team1_id.data == form.team2_id.data:
            flash('Teams cannot play against themselves.', 'danger')
            return render_template('match/edit.html', form=form, match=match, teams=teams)
        match.team1_id = form.team1_id.data
        match.team2_id = form.team2_id.data
        match.score = form.score.data
        match.date = form.date.data
        db.session.commit()
        flash('Match updated successfully!', 'success')
        return redirect(url_for('match.list'))
    return render_template('match/edit.html', form=form, match=match, teams=teams)

@match_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    match = Match.query.get_or_404(id)
    if match.team1.user_id != session['user_id']:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('match.list'))
    db.session.delete(match)
    db.session.commit()
    flash('Match deleted successfully!', 'success')
    return redirect(url_for('match.list'))

@match_bp.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    form = SearchForm()
    matches = []
    if form.validate_on_submit():
        query = f"%{form.query.data}%"
        matches = Match.query.join(Team, Match.team1_id == Team.id).filter(
            (Team.user_id == session['user_id']) & 
            ((Team.name.ilike(query)) | (Match.score.ilike(query)))
        ).all()
    return render_template('match/search.html', form=form, matches=matches)
