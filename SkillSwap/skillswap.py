import streamlit as st
import bcrypt
from user import User, PremiumUser
from database import Database
from payment import Payment

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.user_id = None
    st.session_state.is_premium = False

# Initialize database
db = Database("skillswap.db")

# App title and description
st.title("🤝SkillSwap Exchange Skills, Learn Free!")
st.write("Connect with others to teach and learn skills for free or with premium benefits.")

# Sidebar for navigation
page = st.sidebar.selectbox("Choose a page", ["Home", "Login", "Signup", "Profile", "Swap Skills", "Premium"])

if st.session_state.logged_in:
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user = None
        st.session_state.user_id = None
        st.session_state.is_premium = False
        st.success("Logged out successfully.")


if page == "Home":
    st.header("Welcome to SkillSwap!")
    st.write("Sign up or log in to start exchanging skills like coding, cooking, or graphics design!")
    st.image("images/logo.png", caption="Learn and Teach with SkillSwap!")
    
elif page == "Login":
    st.header("🔐Login")
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")
        if submit:
            user = db.get_user(username)
            if user and bcrypt.checkpw(password.encode('utf-8'), user[3]):   # Check password (index 3)
                st.session_state.logged_in = True
                st.session_state.user_id = user[0]   # Store user ID
                st.session_state.is_premium = user[4]  # Store premium status
                if user[4]:  # is_premium
                    st.session_state.user = PremiumUser(user[1], user[2], None)
                else:
                    st.session_state.user = User(user[1], user[2], user[3])
                st.success(f"✅ Welcome, {username}!")
            else:
                st.error("❌Invalid username or password!")

elif page == "Signup":
    st.header("📝Signup")
    with st.form("signup_form"):
        username = st.text_input("Username")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Signup")
        if submit:
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            if db.add_users(username, email, hashed_password):
                st.success("✅ Signup successfully! Please log in.")
            else:
                st.error("⚠️ Username already exists!")

elif page == "Profile" and st.session_state.logged_in:
    st.header(f"🙍‍♀️ Profile: {st.session_state.user.username}")
    profile = st.session_state.user.display_profile()
    st.write(f"**Email**:{profile['email']}")
    st.write(f"**Skills To Teach**: {','.join(profile['skills_teach']) or 'None'}")
    st.write(f"**Skills To Learn**: {','.join(profile['skills_learn']) or 'None'}")
    if st.session_state.is_premium:
        st.write(f"**Status**: {profile['premium_status']}")

    # Add skills
    st.subheader("➕ Add Skills")
    with st.form("add_skills_form"):
        skill_teach = st.text_input("Skill you can teach (e.g., Python)")
        skill_learn = st.text_input("Skill you want to learn (e.g. , Cooking)")
        submit = st.form_submit_button("Add Skills")
        if submit:
            if skill_teach:
                st.session_state.user.add_skills_teach(skill_teach)
                db.add_skill(st.session_state.user_id, skill_teach, "teach")
                st.success(f"✅ Added {skill_teach} to teachable skills.")
            if skill_learn:
                st.session_state.user.add_skills_learn(skill_learn)
                db.add_skill(st.session_state.user_id, skill_learn, "learn")
                st.success(f"✅ Added {skill_learn} to learnable skills.")

elif page == "Swap Skills" and st.session_state.logged_in:
    st.header("🔄 Swap Skills")
    if st.session_state.is_premium:
        st.write(st.session_state.user.access_premium_features())
        max_swaps = float("inf")  # Unlimited for premium
    else:
        max_swaps = 2  # Limit for free users
        st.write("Free users can swap up to 2 skills. Upgrade to Premium for unlimited swaps!")

    # Display available skills from other users
    st.subheader("🔎 Find Skills To Learn.")
    all_users = db.cursor.execute("SELECT id, username FROM users WHERE id != ?", 
                                  (st.session_state.user_id,)).fetchall()
    
    for user_id, username in all_users:
        skills = db.get_user_skills(user_id, "teach")
        if skills:
            st.write(f"**{username}** offers: {','.join(skills)}")

            # Simplified swap request (no actual matching logic for demo)
            if st.button(f"Request Swap with {username}", key=f"swap_{user_id}"):
                if max_swaps > 0:
                    st.success(f"📩 Swap request sent to {username}!")
                else:
                    st.error("🔒 Upgrade to Premium for more swaps!")

elif page == "Premium" and st.session_state.logged_in:
    st.header("💎 Upgrade To Premium")
    if st.session_state.is_premium:
        st.success("You are already a Premium Member!🌟")
    else:
        st.write("Unlock unlimited skill swaps and priority matching for $5/months")
        payment = Payment(st.session_state.user_id)
        if st.button("Subscribe Now", disabled=st.session_state.get("is_premium", False)):
            result = payment.process_payment()
            if payment.check_subscription():
                db.updated_premium_status(st.session_state.user_id, True)
                st.session_state.is_premium = True
                st.session_state.user = PremiumUser(
                    st.session_state.user.username,
                    st.session_state.user.display_profile()["email"],
                    None
                )
                st.success(result)
            else:
                st.error("🚫 Payment failed! Please try again.")

elif page in ["Profile", "Swap Skills", "Premium"]:
    st.error("Please log in to access this page.")


# Cleanup database connection on app close
def cleanup():
    db.close()

st.markdown("---")
st.caption("Made with 💚 by Areesha Fayyaz 🕊- SkillSwap © 2025")
