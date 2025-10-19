from typing import List, Optional, Dict, Any
from national_agentic_ai_hackathon_2025_backend.database.base import DataBase
from national_agentic_ai_hackathon_2025_backend.schemas.user import User


class UserDB(DataBase):
    """Database operations for User entities"""
    
    def __init__(self):
        super().__init__()
        self.table_name = "users"
    
    async def create_user(self, user: User) -> Dict[str, Any]:
        """
        Create a new user in the database
        
        Args:
            user: User object to create
            
        Returns:
            Dict containing the created user data
        """
        try:
            user_data = user.model_dump()
            result = self.supabase.table(self.table_name).insert(user_data).execute()
            return {"success": True, "data": result.data[0] if result.data else None}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def get_user_by_id(self, userid: str) -> Dict[str, Any]:
        """
        Get a user by their user ID
        
        Args:
            userid: User ID to search for
            
        Returns:
            Dict containing the user data or error
        """
        try:
            result = self.supabase.table(self.table_name).select("*").eq("userid", userid).execute()
            if result.data:
                return {"success": True, "data": result.data[0]}
            else:
                return {"success": False, "error": "User not found"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def get_user_by_phone(self, phone_number: str) -> Dict[str, Any]:
        """
        Get a user by their phone number
        
        Args:
            phone_number: Phone number to search for
            
        Returns:
            Dict containing the user data or error
        """
        try:
            result = self.supabase.table(self.table_name).select("*").eq("phone_number", phone_number).execute()
            if result.data:
                return {"success": True, "data": result.data[0]}
            else:
                return {"success": False, "error": "User not found"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def get_user_by_username(self, username: str) -> Dict[str, Any]:
        """
        Get a user by their username
        
        Args:
            username: Username to search for
            
        Returns:
            Dict containing the user data or error
        """
        try:
            result = self.supabase.table(self.table_name).select("*").eq("username", username).execute()
            if result.data:
                return {"success": True, "data": result.data[0]}
            else:
                return {"success": False, "error": "User not found"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def get_users_by_platform(self, platform: str, limit: int = 100) -> Dict[str, Any]:
        """
        Get users by platform (website or whatsapp)
        
        Args:
            platform: Platform to filter by
            limit: Maximum number of results
            
        Returns:
            Dict containing list of users
        """
        try:
            result = self.supabase.table(self.table_name).select("*").eq(
                "platform", platform
            ).limit(limit).execute()
            return {"success": True, "data": result.data if result.data else []}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def get_logged_in_users(self, limit: int = 100) -> Dict[str, Any]:
        """
        Get all currently logged in users
        
        Args:
            limit: Maximum number of results
            
        Returns:
            Dict containing list of logged in users
        """
        try:
            result = self.supabase.table(self.table_name).select("*").eq(
                "is_loggedin", True
            ).limit(limit).execute()
            return {"success": True, "data": result.data if result.data else []}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def update_user(self, userid: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update a user's information
        
        Args:
            userid: User ID of the user to update
            updates: Dictionary of fields to update
            
        Returns:
            Dict containing success status and updated data
        """
        try:
            result = self.supabase.table(self.table_name).update(updates).eq(
                "userid", userid
            ).execute()
            
            if result.data:
                return {"success": True, "data": result.data[0]}
            else:
                return {"success": False, "error": "User not found or no changes made"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def update_user_login_status(self, userid: str, is_loggedin: bool) -> Dict[str, Any]:
        """
        Update a user's login status
        
        Args:
            userid: User ID of the user to update
            is_loggedin: New login status
            
        Returns:
            Dict containing success status and updated data
        """
        try:
            result = self.supabase.table(self.table_name).update({
                "is_loggedin": is_loggedin
            }).eq("userid", userid).execute()
            
            if result.data:
                return {"success": True, "data": result.data[0]}
            else:
                return {"success": False, "error": "User not found"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def update_user_password(self, userid: str, new_password: str) -> Dict[str, Any]:
        """
        Update a user's password
        
        Args:
            userid: User ID of the user to update
            new_password: New password
            
        Returns:
            Dict containing success status
        """
        try:
            result = self.supabase.table(self.table_name).update({
                "password": new_password
            }).eq("userid", userid).execute()
            
            if result.data:
                return {"success": True, "message": "Password updated successfully"}
            else:
                return {"success": False, "error": "User not found"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def delete_user(self, userid: str) -> Dict[str, Any]:
        """
        Delete a user from the database
        
        Args:
            userid: User ID of the user to delete
            
        Returns:
            Dict containing success status
        """
        try:
            result = self.supabase.table(self.table_name).delete().eq(
                "userid", userid
            ).execute()
            
            if result.data:
                return {"success": True, "message": "User deleted successfully"}
            else:
                return {"success": False, "error": "User not found"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def search_users(self, query: str, limit: int = 50) -> Dict[str, Any]:
        """
        Search users by username or phone number
        
        Args:
            query: Search query string
            limit: Maximum number of results
            
        Returns:
            Dict containing list of matching users
        """
        try:
            result = self.supabase.table(self.table_name).select("*").or_(
                f"username.ilike.%{query}%,phone_number.ilike.%{query}%"
            ).limit(limit).execute()
            return {"success": True, "data": result.data if result.data else []}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def get_all_users(self, limit: int = 100, offset: int = 0) -> Dict[str, Any]:
        """
        Get all users with pagination
        
        Args:
            limit: Maximum number of results
            offset: Number of results to skip
            
        Returns:
            Dict containing list of users
        """
        try:
            result = self.supabase.table(self.table_name).select("*").range(
                offset, offset + limit - 1
            ).execute()
            return {"success": True, "data": result.data if result.data else []}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def authenticate_user(self, username: str, password: str) -> Dict[str, Any]:
        """
        Authenticate a user with username and password
        
        Args:
            username: Username to authenticate
            password: Password to verify
            
        Returns:
            Dict containing authentication result and user data
        """
        try:
            result = self.supabase.table(self.table_name).select("*").eq(
                "username", username
            ).eq("password", password).execute()
            
            if result.data:
                # Update login status
                await self.update_user_login_status(result.data[0]["userid"], True)
                return {"success": True, "data": result.data[0], "message": "Authentication successful"}
            else:
                return {"success": False, "error": "Invalid credentials"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def logout_user(self, userid: str) -> Dict[str, Any]:
        """
        Logout a user by updating their login status
        
        Args:
            userid: User ID to logout
            
        Returns:
            Dict containing success status
        """
        try:
            result = await self.update_user_login_status(userid, False)
            if result["success"]:
                return {"success": True, "message": "User logged out successfully"}
            else:
                return result
        except Exception as e:
            return {"success": False, "error": str(e)}