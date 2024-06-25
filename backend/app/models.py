from . import db

class Users(db.Model):
    userId = db.Column(db.String(255), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    passwordHash = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    income = db.Column(db.Float, nullable=False)
    creditCardLimit = db.Column(db.Float, nullable=False)
    financialGoals = db.Column(db.Text, nullable=True)
    address = db.Column(db.Text, nullable=True)
    phone = db.Column(db.String(255), nullable=True)
    accountCreationDate = db.Column(db.Date, nullable=False)

class Transactions(db.Model):
    transactionId = db.Column(db.String(255), primary_key=True)
    userId = db.Column(db.String(255), db.ForeignKey('user.userId'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    description = db.Column(db.Text, nullable=True)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(255), nullable=False)
    mcc = db.Column(db.String(255), nullable=False)
    merchantName = db.Column(db.String(255), nullable=True)
    merchantCity = db.Column(db.String(255), nullable=True)
    merchantCountry = db.Column(db.String(255), nullable=True)
    paymentMethod = db.Column(db.String(255), nullable=False)

class EmissionFactors(db.Model):
    categoryId = db.Column(db.String(255), primary_key=True)
    categoryName = db.Column(db.String(255), nullable=False)
    emissionFactor = db.Column(db.Float, nullable=False)

class MonthlyUserEmissions(db.Model):
    userId = db.Column(db.String(255), primary_key=True)
    date = db.Column(db.Date, primary_key=True)
    category = db.Column(db.String(255), primary_key=True)
    emission = db.Column(db.Float, nullable=False)

class MonthlyRecommendations(db.Model):
    userId = db.Column(db.String(255), primary_key=True)
    date = db.Column(db.Date, primary_key=True)
    project = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    rating = db.Column(db.Integer, nullable=True)

class ProjectDetails(db.Model):
    projectId = db.Column(db.String(255), primary_key=True)
    projectName = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
