import streamlit as st
import sqlite3
import hashlib

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    
st.set_page_config(page_title="RMS",page_icon="🎵",initial_sidebar_state="expanded")

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

if st.session_state.get('logged_in', False):
    st.sidebar.title(f"Hello, {st.session_state.user['username']}")
    menu = st.sidebar.selectbox('Menu', ['Update Info', 'Delete Account'])

    # 회원 정보 수정 처리
    if menu == 'Update Info':
        st.title("Update Info")
        
        username = st.text_input("Username", placeholder="Enter your username", key="update_username")
        old_pw = st.text_input("Current Password", type="password", placeholder="Enter your current password")
        new_pw = st.text_input("New Password", type="password", placeholder="Enter a new password")
        confirm_pw = st.text_input("Confirm New Password", type="password", placeholder="Re-enter your new password")
        new_email = st.text_input("New Email", placeholder="Enter your new email")
        
        update_btn = st.button("Update Info")
        
        if update_btn:
            if new_pw != confirm_pw:
                st.error("New passwords do not match")
            else:
                conn = sqlite3.connect('./db.db')
                cursor = conn.cursor()
                
                cursor.execute("SELECT * FROM user WHERE username = ?", (username,))
                row = cursor.fetchone()
                
                if row is None:
                    st.error("Username does not exist")
                else:
                    db_pw = row[2]
                    if db_pw == hash_password(old_pw):
                        hashed_new_pw = hash_password(new_pw)
                        cursor.execute("UPDATE user SET password = ?, email = ? WHERE username = ?", 
                                        (hashed_new_pw, new_email, username))
                        conn.commit()
                        st.success("Information updated successfully")
                    else:
                        st.error("Current password is incorrect")
                
                conn.close()
                
    # 회원 탈퇴 처리
    elif menu == 'Delete Account':
        st.title("Delete Account")
        
        username = st.text_input("Username", placeholder="Enter your username")
        pw = st.text_input("Password", type="password", placeholder="Enter your password")
        delete_btn = st.button("Delete Account")
        
        if delete_btn:
            conn = sqlite3.connect('./db.db')
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM user WHERE username = ?", (username,))
            row = cursor.fetchone()
            
            if row is None:
                st.error("Username does not exist")
            else:
                db_pw = row[2]
                if db_pw == hash_password(pw):
                    cursor.execute("DELETE FROM user WHERE username = ?", (username,))
                    conn.commit()
                    st.success("Account deleted successfully")
                else:
                    st.error("Password is incorrect")
            
            conn.close()
else:
    menu = st.sidebar.selectbox("Menu", ['Sign in', 'Register', 'Update Info', 'Delete Account'])

    if menu == 'Sign in':
        # 데이터 베이스 연결
        conn = sqlite3.connect('./db.db')
        cursor = conn.cursor()
        
        st.title("Sign in")
        username = st.text_input("Username", placeholder="Enter a username", key="sign_in_username")
        pw = st.text_input("Password", type="password", placeholder="Enter a password", key="sign_in_pw")
        btn = st.button("Sign in")
        
        # 로그인 버튼을 클릭
        if btn:        
            # DB에서 (입력한 아이디) 정보를 가져온다
            cursor.execute("SELECT * FROM user WHERE username = ?", (username,))
            row = cursor.fetchone()
            # 비밀번호 일치여부 확인
            if row == None:
                st.error("The username does not exist.")
            else:
                db_id = row[1]
                db_pw = row[2]
                
                if db_pw == hash_password(pw):
                    # 로그인 성공 시
                    st.session_state.logged_in = True
                    st.session_state.user = {
                        'userid': row[0],  # Assuming userid is at index 0
                        'username': row[1],
                        'email': row[3],  # Assuming email is at index 3
                        'gender': row[4],  # Assuming gender is at index 4
                        'created_at': row[5]  # Assuming created_at is at index 5
                    }
                    st.success("Sign in Success")
                else:
                    # 로그인 실패시 로그인 실패
                    st.error("Sign in failed")
                    
        conn.close()
        
    elif menu == 'Register':
        # 회원가입 화면
        st.title("Register")
        
        new_username = st.text_input("Username", placeholder="Enter a username")
        new_pw = st.text_input("Password", type="password", placeholder="Enter a password")
        confirm_pw = st.text_input("Confirm Password", type="password", placeholder="Re-enter your password")
        email = st.text_input("Email", placeholder="Enter your email")
        
        gender = st.radio("Gender", ['Male', 'Female', 'Other'])
        register_btn = st.button("Register")
        
        if register_btn:
            if new_pw != confirm_pw:
                st.error("Passwords do not match")
            else:
                conn = sqlite3.connect('./db.db')
                cursor = conn.cursor()
                
                try:
                    hashed_pw = hash_password(new_pw)
                    cursor.execute("INSERT INTO user (username, password, email, gender) VALUES (?, ?, ?, ?)", 
                                    (new_username, hashed_pw, email, gender))
                    conn.commit()
                    st.success("Registration successful! Please sign in.")
                except sqlite3.IntegrityError:
                    st.error("Username already exists. Please choose a different one.")
                
                # 데이터베이스 연결 종료
                conn.close()
            
    # 회원 정보 수정 처리
    elif menu == 'Update Info':
        st.title("Update Info")
        
        username = st.text_input("Username", placeholder="Enter your username", key="update_username")
        old_pw = st.text_input("Current Password", type="password", placeholder="Enter your current password")
        new_pw = st.text_input("New Password", type="password", placeholder="Enter a new password")
        confirm_pw = st.text_input("Confirm New Password", type="password", placeholder="Re-enter your new password")
        new_email = st.text_input("New Email", placeholder="Enter your new email")
        
        update_btn = st.button("Update Info")
        
        if update_btn:
            if new_pw != confirm_pw:
                st.error("New passwords do not match")
            else:
                conn = sqlite3.connect('./db.db')
                cursor = conn.cursor()
                
                cursor.execute("SELECT * FROM user WHERE username = ?", (username,))
                row = cursor.fetchone()
                
                if row is None:
                    st.error("Username does not exist")
                else:
                    db_pw = row[2]
                    if db_pw == hash_password(old_pw):
                        hashed_new_pw = hash_password(new_pw)
                        cursor.execute("UPDATE user SET password = ?, email = ? WHERE username = ?", 
                                        (hashed_new_pw, new_email, username))
                        conn.commit()
                        st.success("Information updated successfully")
                    else:
                        st.error("Current password is incorrect")
                
                conn.close()
                
    # 회원 탈퇴 처리
    elif menu == 'Delete Account':
        st.title("Delete Account")
        
        username = st.text_input("Username", placeholder="Enter your username")
        pw = st.text_input("Password", type="password", placeholder="Enter your password")
        delete_btn = st.button("Delete Account")
        
        if delete_btn:
            conn = sqlite3.connect('./db.db')
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM user WHERE username = ?", (username,))
            row = cursor.fetchone()
            
            if row is None:
                st.error("Username does not exist")
            else:
                db_pw = row[2]
                if db_pw == hash_password(pw):
                    cursor.execute("DELETE FROM user WHERE username = ?", (username,))
                    conn.commit()
                    st.success("Account deleted successfully")
                else:
                    st.error("Password is incorrect")
            
            conn.close()