document.addEventListener("DOMContentLoaded", function() {
    const payNowButton = document.getElementById('payBtn');
    
    if (payNowButton) {
      payNowButton.addEventListener("click", function() {

        const emailInput = document.getElementById('email');
        const password = document.getElementById('password').value;
        const email = emailInput.value.trim();
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        const api_url_post = "https://softwareai.rshare.io/create-checkout";

        if (!email) {
          alert('Please enter your email address');
          emailInput.focus();
          return;
        }
        
        if (!emailRegex.test(email)) {
          alert('Please enter a valid email address');
          emailInput.focus();
          return;
        }
        
        if (!password) {
          alert("Please enter your password.");
          return; 
        }

        fetch(api_url_post, {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            email: email,
            password: password,
          }),
        })
        .then(response => {
          console.log("Resposta do servidor:", response);
        
          if (!response.ok) {
            throw new Error("Erro na requisição. Status: " + response.status);
          }
          return response.json()
            .catch(error => {
              console.error("Erro ao converter a resposta para JSON:", error);
              throw new Error("Erro ao converter a resposta para JSON");
            });
        })
        .then(data => {
          console.log("Dados recebidos:", data); 
        
          if (data.sessionId) {
            const stripe = Stripe("pk_test_51QpX90Cvm2cRLHtdoF7n2Ea4sRRjYBx8Csiii0e6M6ECTJJ8fKaQ1DKpJApfJZH5hIkWRojaMmaxY9sEcS50tspB00DF2IA12h");
            stripe.redirectToCheckout({ sessionId: data.sessionId })
            .then(() => {
              window.location.href = "https://softwareai.rshare.io/checkout/sucess"; 
            });
          } else {
            alert("Erro ao criar a sessão de pagamento.");
          }
        })
        .catch(error => {
          console.error("Erro ao enviar a requisição:", error);
          alert("Erro ao processar o pagamento.");
        });

      });
    }
});
