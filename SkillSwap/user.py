# class for User

class User:
    def __init__(self, username, email, password):
        self._username = username   # protected attributes
        self._email = email
        self._password = password 

        self._skills_teach = []  # Skills the user can teach
        self._skills_learn = []  # skils the user want to learn

    def add_skills_teach(self, skills):
        self._skills_teach.append(skills)
        return f"{skills} added to teachable skills."

    def add_skills_learn(self, skills):
        self._skills_learn.append(skills)
        return f"{skills} added to learnable skills."
    
    def display_profile(self):
        return {
            "username" : self._username,
            "email" : self._email,
            "skills_teach" : self._skills_teach,
            "skills_learn" : self._skills_learn
        }
    
    @property
    def username(self):
        return self._username
    
# for PremiumUsers

class PremiumUser(User):
    def __init__(self, username, email, password):
        super().__init__(username, email, password)
        self._is_premium = True

    def display_profile(self):
        profile = super().display_profile()
        profile["premium_status"] = "Premium Member"
        return profile
    
    def access_premium_features(self):
        return "Access to unlimited skill swaps and priority matching!"
    
