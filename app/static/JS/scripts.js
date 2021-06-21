const btn = document.getElementById("analyze-button");
const grammarSection = document.getElementById("analyze-section");
const clearIcon = document.getElementById("clear-icon");
const clearText = document.getElementById("analyze-text");
const grammarText = document.getElementById("prtext");
if (btn) {
  btn.addEventListener("click", () => {
    if (clearText.innerText == "გაანალიზე") {
      if (prtext.value.trim().length == 0) {
        alert("გთხოვთ, შეიყვანეთ ტექსტი.");
      } else {
        grammarSection.classList.toggle("display-flex");
        clearText.innerText = "გაასუფთავე";
        clearIcon.classList.toggle("display-flex");
        btn.style.background = "#707070";
        btn.style.padding = "8px";
      }
    } else {
      clearIcon.classList.toggle("display-flex");
      grammarSection.classList.toggle("display-flex");
      clearText.innerText = "გაანალიზე";
      btn.style.background = "#172224";
      btn.style.padding = "8px 42px";
      btn.classList.remove("clear-bt");
      grammarText.value = "";
    }
  });
}

const loginBtn = document.querySelector(".login");
const loginContent = document.querySelector(".login-bg");

const loginEvent = () => {
  loginContent.classList.add("active-login");
  recovPas.classList.remove("active-login");
};
loginBtn.addEventListener("click", loginEvent);

loginForm = document.getElementById("login-form");
loginForm.addEventListener("submit", (e) => {
  e.preventDefault();
  const divEmail = document.querySelector(".email-input");
  const divPassword = document.querySelector(".password-input");
  let inputEmail = document.forms["login"]["email"].value;
  let inputPassword = document.forms["login"]["password"].value;
  const emailContext = () => {
    if (divEmail.childNodes[3] === undefined) {
      const validEdiv = document.createElement("span");
      validEdiv.classList.add("emailwarning");
      validEdiv.textContent = "გთხოვთ შეიყვანეთ მეილი";
      divEmail.append(validEdiv);
    }
  };
  const passwordContext = () => {
    if (divPassword.childNodes[3] === undefined) {
      const validPdiv = document.createElement("span");
      validPdiv.classList.add("passwordvalidation");
      validPdiv.textContent = "გთხოვთ შეიყვანეთ პაროლი";
      divPassword.append(validPdiv);
    }
  };

  if (inputEmail == "" && inputPassword == "") {
    emailContext();
    passwordContext();
    return false;
  } else if (inputPassword == "" && inputEmail !== "") {
    if (divEmail.childNodes[3] !== undefined) {
      divEmail.childNodes[3].remove();
    }
    passwordContext();
    return false;
  } else if (inputPassword !== "" && inputEmail == "") {
    emailContext();
    if (divPassword.childNodes[3] !== undefined) {
      divPassword.childNodes[3].remove();
    }
    return false;
  } else {
    localStorage.setItem(
      "loginInfo",
      JSON.stringify({ email: inputEmail, password: inputPassword })
    );
    location.reload();
  }
});

const loginLogo = document.querySelector(".user-logo");

const dropDown = () => {
  const userName = JSON.parse(localStorage.getItem("loginInfo")).email.split(
    "@"
  )[0];
  const dropdown = document.querySelector("#dropdown");
  const userInfo = document.querySelector("#user-name");
  userInfo.innerText = userName;
  dropdown.classList.toggle("active-dropdown");
  loginLogo.classList.toggle("invertedLogo");
  loginBtn.classList.toggle("dropdownMargin");
};

const userLogged = () => {
  loginLogo.src = "../assets/dif-head-logo.svg";
  loginBtn.removeEventListener("click", loginEvent);
  loginLogo.addEventListener("click", dropDown);
};

if (localStorage.loginInfo) {
  userLogged();
}

const logout = document.querySelector("#log-out");

logout.addEventListener("click", () => {
  localStorage.removeItem("loginInfo");
  location.reload();
});

const addButton = document.querySelector("#add-file");
if (addButton) {
  addButton.addEventListener("click", () => {
    window.location.href = "add-file.html";
  });
}

const copyInp = document.querySelector(".copy-inp");
const arrowInc = document.querySelector(".arrow-increase");
const up = document.querySelector(".cont-up");
const uploadFile = document.querySelector(".upload-file");
const flName = document.querySelector(".file-name");

if (arrowInc) {
  arrowInc.addEventListener("click", () => {
    if (!copyInp.classList.contains("active-textarea")) {
      if (flName.textContent == "") {
        copyInp.style.height = "352px";
        arrowInc.style.transform = "rotate(270deg)";
        up.style.display = "none";
        uploadFile.style.display = "none";
        copyInp.classList.add("active-textarea");
      }
    } else {
      copyInp.classList.remove("active-textarea");
      copyInp.style.height = "70px";
      arrowInc.style.transform = "rotate(0deg)";
      up.style.display = "block";
      uploadFile.style.display = "block";
    }
  });

  copyInp.addEventListener("click", () => {
    if (flName.textContent == "") {
      copyInp.style.height = "352px";
      arrowInc.style.transform = "rotate(270deg)";
      up.style.display = "none";
      uploadFile.style.display = "none";
      copyInp.classList.add("active-textarea");
    }
  });
}

const uploadBtn = document.querySelector("#btn-upload");
if (uploadBtn) {
  const inputFile = document.querySelector("#file-input");
  const copyHead = document.querySelector("#copy-text-head");
  const copyCont = document.querySelector(".copy-container");
  uploadBtn.addEventListener("click", () => {
    inputFile.classList.toggle("display-block");
  });
  inputFile.onchange = () => {
    copyHead.style.display = "none";
    copyCont.style.display = "none";
  };
}
const regButton = document.querySelector(".registration-button");
const login = document.querySelector(".login-content");
const registration = document.querySelector(".registration-content");
const logBtn = document.querySelector(".avtorization-button");

regButton.addEventListener("click", () => {
  login.classList.add("invisible");
  registration.classList.remove("invisible");
  registration.classList.add("visible");
});

logBtn.addEventListener("click", () => {
  registration.classList.remove("visible");
  registration.classList.add("invisible");
  login.classList.remove("invisible");
  login.classList.add("visible");
});

const recovPas = document.querySelector(".pas-rec-bg");
const forgotBtn = document.querySelector(".forgot-password");

forgotBtn.addEventListener("click", (e) => {
  e.preventDefault();
  recovPas.classList.remove("invisible");
  recovPas.classList.add("visible");
  login.classList.add("invisible");
});

window.onclick = (event) => {
  if (event.target == loginContent) {
    loginContent.classList.remove("active-login");
    recovPas.classList.add("invisible");
    recovPas.classList.remove("visible");
    login.classList.remove("invisible");
    login.classList.add("visible");
    registration.classList.add("invisible");
    registration.classList.remove("visible");
  }
};

const regForm = document.getElementById("registration-form");

regForm.addEventListener("submit", (e) => {
  e.preventDefault();
  const divEmail = document.querySelector(".reg-email-input");
  const divPassword = document.querySelector(".reg-password-input");
  const divPasswordRep = document.querySelector(".reg-password-input-rep");
  let inputEmail = document.forms["registration"]["email"].value;
  let inputPassword = document.forms["registration"]["password"].value;
  let inputPasswordRep = document.forms["registration"]["passwordrep"].value;
  const emailContext = () => {
    if (divEmail.childNodes[3] === undefined) {
      const validEdiv = document.createElement("span");
      validEdiv.classList.add("emailwarning");
      validEdiv.textContent = "გთხოვთ შეიყვანეთ მეილი";
      divEmail.append(validEdiv);
    }
  };
  const passwordContext = () => {
    if (divPassword.childNodes[3] === undefined) {
      const validPdiv = document.createElement("span");
      validPdiv.classList.add("passwordvalidation");
      validPdiv.textContent = "გთხოვთ შეიყვანეთ პაროლი";
      divPassword.append(validPdiv);
    }
  };

  const passwordContextRepeat = () => {
    if (divPasswordRep.childNodes[3] === undefined) {
      const validPdiv = document.createElement("span");
      validPdiv.classList.add("passwordvalidation");
      validPdiv.textContent = "გთხოვთ შეიყვანეთ პაროლი";
      divPasswordRep.append(validPdiv);
    }
  };

  if (inputEmail == "" && inputPassword == "" && inputPasswordRep == "") {
    emailContext();
    passwordContext();
    passwordContextRepeat();
    return false;
  } else if (
    inputPassword == "" &&
    inputEmail !== "" &&
    inputPasswordRep !== ""
  ) {
    if (divEmail.childNodes[3] !== undefined) {
      divEmail.childNodes[3].remove();
    }
    if (divPasswordRep.childNodes[3] !== undefined) {
      divPasswordRep.childNodes[3].remove();
    }
    passwordContext();
    return false;
  } else if (
    inputPassword == "" &&
    inputEmail == "" &&
    inputPasswordRep !== ""
  ) {
    if (divEmail.childNodes[3] !== undefined) {
      divEmail.childNodes[3].remove();
    }
    if (divPasswordRep.childNodes[3] !== undefined) {
      divPasswordRep.childNodes[3].remove();
    }
    passwordContext();
    emailContext();
    return false;
  } else if (
    inputPassword == "" &&
    inputPasswordRep == "" &&
    inputEmail !== ""
  ) {
    if (divEmail.childNodes[3] !== undefined) {
      divEmail.childNodes[3].remove();
    }
    passwordContext();
    passwordContextRepeat();
    return false;
  } else if (inputEmail !== "" && inputPasswordRep == "" && inputEmail !== "") {
    if (divEmail.childNodes[3] !== undefined) {
      divEmail.childNodes[3].remove();
    }
    if (divPassword.childNodes[3] !== undefined) {
      divPassword.childNodes[3].remove();
    }
    passwordContextRepeat();
    return false;
  } else if (
    inputEmail == "" &&
    inputPasswordRep !== "" &&
    inputPassword !== ""
  ) {
    if (divPassword.childNodes[3] !== undefined) {
      divPassword.childNodes[3].remove();
    }
    if (divPasswordRep.childNodes[3] !== undefined) {
      divPasswordRep.childNodes[3].remove();
    }
    emailContext();
    return false;
  } else if (
    inputEmail == "" &&
    inputPasswordRep == "" &&
    inputPassword !== ""
  ) {
    if (divPassword.childNodes[3] !== undefined) {
      divPassword.childNodes[3].remove();
    }
    passwordContextRepeat();
    emailContext();
    return false;
  } else if (
    inputEmail !== "" &&
    inputPasswordRep !== "" &&
    inputEmail !== ""
  ) {
    if (divEmail.childNodes[3] !== undefined) {
      divEmail.childNodes[3].remove();
    }
    if (divPassword.childNodes[3] !== undefined) {
      divPassword.childNodes[3].remove();
    }
    if (divPasswordRep.childNodes[3] !== undefined) {
      divPasswordRep.childNodes[3].remove();
    }
    location.reload();
    return true;
  }
});

const upload = document.querySelector(".btn-upload");
let fileName;

upload.addEventListener("change", (item) => {
  fileName = upload.value.split("\\").slice(-1)[0];
  flName.innerHTML = fileName;
  if (flName.textContent !== "") {
    copyInp.disabled = true;
  }
});
