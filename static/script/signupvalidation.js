function validateForm() 
{
  
  var retValue = true;
  // בדיקות שם משתמש
  if (!validateUsername()) 
  {
      retValue = false; 
  } 
  // בדיקות סיסמא  
  if(!validatePassword()) 
  {
      retValue = false; 
  }
  // בדיקת סיסמא חוזרת  
  if(!validateRepeatPassword()) 
  {
      retValue = false; 
  }  
  
  return retValue;
}

// בדיקות חוקיות שם משתמש:
// לפחות 6 תווים
// חייב להתחיל באות באנגלית (קטנה או גדולה)
function validateUsername()
{
  var username = document.getElementById("username").value;
  var usernameError = document.getElementById("username-error");
  var nameStartLetterRegex = /^[a-zA-Z]/;
    
  if(username.length < 6)
  {
      usernameError.innerText = "name must be at least 6 characters long.";
      return false;
  }
  else if(!nameStartLetterRegex.test(username))
  {
      usernameError.innerText = "name must start with a letter.";
      return false;
  }
  else {
      usernameError.innerText = "";
  }
  return true;
}
// בדיקת חוקיות סיסמא:
// חייבת להכיל לפחות ספרה אחת
// חייבת להכיל לפחות "תו מיוחד" אחד
function validatePassword() 
{
    var password = document.getElementById("password").value;
    var errorMessage = document.getElementById("password-error");

    // Password validation
    var passwordincludeDigitRegex = /\d/; // regular expression - check that password include at least 1 digit
    var passwordSpecialCharRegex = /[@$!%*?&]/; // regular expression - check that password include at least 1 special character

    if (!passwordincludeDigitRegex.test(password)) {
        errorMessage.innerText = "Password must include at least one digit.";
        return false;
    } else if (!passwordSpecialCharRegex.test(password)) {
        errorMessage.innerText = "Password must include at least one special character.";
        return false;
    } else if(password.length < 7)
    {
        errorMessage.innerText = "Password must be at least 7 characters long.";
        return false;
    } else {
        errorMessage.innerText = "";
    }
    return true;
}

// בדיקה שסיסמא זהה לסיסמא חוזרת
// 
function validateRepeatPassword() 
{
    var password = document.getElementById("password").value;
    var repeatPassword = document.getElementById("repeat-password").value;
    var errorMessage = document.getElementById("repeat-password-error");

    if (password != repeatPassword) {
        errorMessage.innerText = "Passwords do not match.";
        return false;
    } else {
        errorMessage.innerText = "";
    }
    return true;
}

// פונקציה שמאפשרת למשתמש לראות את הסיסמא
function togglePassword() {
    var passwordInput = document.getElementById("password");
    if (passwordInput.type === "password") {
        passwordInput.type = "text";
    } else {
        passwordInput.type = "password";
    }
}
