    const signInBtn = document.getElementById("signIn");
    const signUpBtn = document.getElementById("signUp");
    const fistForm = document.getElementById("form1");
    const secondForm = document.getElementById("form2");
    const container = document.querySelector(".container");

    // right-panel-active
    signInBtn.addEventListener("click", () => {
      container.classList.remove("container");
    });

    signUpBtn.addEventListener("click", () => {
      container.classList.add("container");
    });

    fistForm.addEventListener("submit", (e) => e.preventDefault());
    secondForm.addEventListener("submit", (e) => e.preventDefault());
