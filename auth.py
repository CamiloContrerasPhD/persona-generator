import os
import streamlit as st
import pandas as pd
import bcrypt
from typing import Optional, Dict, Any
from datetime import datetime


class ExcelAuth:
    def __init__(self, users_file: str = "users.xlsx"):
        self.users_file = users_file
        self.users_df = self._load_users()
    
    def _load_users(self) -> pd.DataFrame:
        """Load users from Excel file or Streamlit secrets"""
        # Try to load from Streamlit secrets first (for production)
        try:
            if hasattr(st, 'secrets') and hasattr(st.secrets, 'users_data'):
                users_data = st.secrets['users_data']
                if isinstance(users_data, list):
                    df = pd.DataFrame(users_data)
                    # Ensure required columns exist
                    required_cols = ['email', 'password_hash', 'created_at', 'last_login']
                    for col in required_cols:
                        if col not in df.columns:
                            df[col] = None
                    return df
        except Exception:
            # Silently fall back to local file - no warning needed
            pass
        
        # Fallback to local Excel file (for development)
        if os.path.exists(self.users_file):
            try:
                df = pd.read_excel(self.users_file)
                # Ensure required columns exist
                required_cols = ['email', 'password_hash', 'created_at', 'last_login']
                for col in required_cols:
                    if col not in df.columns:
                        df[col] = None
                return df
            except Exception as e:
                st.error(f"Error loading users file: {e}")
                return pd.DataFrame(columns=['email', 'password_hash', 'created_at', 'last_login'])
        else:
            # Create empty DataFrame with required columns
            return pd.DataFrame(columns=['email', 'password_hash', 'created_at', 'last_login'])
    
    def _save_users(self):
        """Save users to Excel file (only works in development)"""
        # Only save to Excel file in development (not in production with secrets)
        try:
            if hasattr(st, 'secrets') and hasattr(st.secrets, 'users_data'):
                # In production with secrets, don't save
                pass
            else:
                # In development, save to Excel
                self.users_df.to_excel(self.users_file, index=False)
        except Exception as e:
            st.error(f"Error saving users file: {e}")
    
    def _hash_password(self, password: str) -> str:
        """Hash password using bcrypt"""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    def _verify_password(self, password: str, hashed: str) -> bool:
        """Verify password against hash"""
        try:
            return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
        except Exception:
            return False
    
    def register_user(self, email: str, password: str) -> bool:
        """Register a new user (DISABLED - only predefined users allowed)"""
        st.error("❌ Registro deshabilitado. Solo usuarios predefinidos pueden acceder.")
        return False
    
    def authenticate_user(self, email: str, password: str) -> Optional[Dict[str, Any]]:
        """Authenticate user with email and password"""
        email = email.lower().strip()
        
        # Find user
        user_row = self.users_df[self.users_df['email'] == email]
        if user_row.empty:
            return None
        
        # Verify password
        stored_hash = user_row.iloc[0]['password_hash']
        if not self._verify_password(password, stored_hash):
            return None
        
        # Update last login
        self.users_df.loc[self.users_df['email'] == email, 'last_login'] = datetime.now().isoformat()
        self._save_users()
        
        return {
            'email': email,
            'created_at': user_row.iloc[0]['created_at'],
            'last_login': datetime.now().isoformat()
        }
    
    def get_all_users(self) -> pd.DataFrame:
        """Get all users (for admin purposes)"""
        return self.users_df.copy()
    
    def delete_user(self, email: str) -> bool:
        """Delete a user"""
        email = email.lower().strip()
        if email not in self.users_df['email'].values:
            return False
        
        self.users_df = self.users_df[self.users_df['email'] != email]
        self._save_users()
        return True


def init_auth_session():
    """Initialize authentication session state"""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "user_info" not in st.session_state:
        st.session_state.user_info = None


def login_required(func):
    """Decorator to require authentication for Streamlit pages"""
    def wrapper(*args, **kwargs):
        init_auth_session()
        
        if not st.session_state.authenticated:
            st.error("🔒 Acceso restringido - Debes iniciar sesión")
            st.info("Por favor, inicia sesión con tu email y contraseña")
            
            # Show login form
            show_login_form()
            return
        
        return func(*args, **kwargs)
    return wrapper


def show_login_form():
    """Show login form"""
    with st.form("login_form"):
        st.subheader("Iniciar Sesión")
        email = st.text_input("Email", placeholder="tu@email.com")
        password = st.text_input("Contraseña", type="password")
        
        login_submitted = st.form_submit_button("Iniciar Sesión")
        
        if login_submitted:
            if email and password:
                auth = ExcelAuth()
                user_info = auth.authenticate_user(email, password)
                
                if user_info:
                    st.session_state.authenticated = True
                    st.session_state.user_info = user_info
                    st.success(f"✅ Bienvenido, {user_info['email']}")
                    st.rerun()
                else:
                    st.error("❌ Email o contraseña incorrectos")
            else:
                st.error("Por favor completa todos los campos")
        
        # Mostrar usuarios disponibles (sin contraseñas)
        st.markdown("---")
        st.markdown("**👥 Usuarios disponibles:**")
        st.markdown("📧 admin@test.com")
        st.markdown("📧 usuario@test.com")


def logout():
    """Logout user and clear session"""
    st.session_state.authenticated = False
    st.session_state.user_info = None
    st.rerun()


def show_admin_panel():
    """Show admin panel for user management (read-only)"""
    if not st.session_state.authenticated:
        return
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("👥 Usuarios del Sistema")
    
    auth = ExcelAuth()
    users_df = auth.get_all_users()
    
    if not users_df.empty:
        st.sidebar.markdown("**Usuarios disponibles:**")
        for _, user in users_df.iterrows():
            email = user['email']
            created = user['created_at'][:10] if user['created_at'] and str(user['created_at']) != 'nan' else 'N/A'
            last_login = user['last_login'][:10] if user['last_login'] and str(user['last_login']) != 'nan' else 'Nunca'
            
            st.sidebar.markdown(f"📧 {email}")
            st.sidebar.markdown(f"   📅 Creado: {created}")
            st.sidebar.markdown(f"   🔄 Último login: {last_login}")
    else:
        st.sidebar.info("No hay usuarios registrados")
