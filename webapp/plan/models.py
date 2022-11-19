from webapp import db


class Plan(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    company = db.relationship("Company", back_populates="plan")
    viewplan = db.relationship("ViewPlan", back_populates="plan")

    def __repr__(self):
        return '<Plan {}>'.format(self.name)

    def change_attributes(self, form):
        self.name = form.name.data

    def get_name(self):
        return self.name


class View(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    icon = db.Column(db.String(50), nullable=False)
    url = db.Column(db.String(50), nullable=False)
    viewplan = db.relationship("ViewPlan", back_populates="view")
    viewrole = db.relationship("ViewRole", back_populates="view")

    def __repr__(self):
        return '<View {}>'.format(self.name)

    def change_attributes(self, form):
        self.name = form.name.data
        self.icon = form.icon.data
        self.url = form.url.data

    def get_name(self):
        return self.name




class ViewPlan(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    active = db.Column(db.Boolean, default=False)

    plan_id = db.Column(db.Integer(), db.ForeignKey("plan.id"))
    plan = db.relationship("Plan", back_populates="viewplan")
    view_id = db.Column(db.Integer(), db.ForeignKey("view.id"))
    view = db.relationship("View", back_populates="viewplan")

    def __repr__(self):
        return '<ViewPlan {}>'.format(self.id)

    def change_attributes(self, form):
        self.plan_id = form.plan.data
        self.view_id = form.view.data

    def get_name_view(self, id):
        view = View.query.filter_by(id=id).first()
        return view.get_name()

    def change_active(self):
        if self.active:
            self.active = False
        else:
            self.active = True



