let toastTimer = null;

async function addToCart(id, btn) {
  if (btn) { btn.disabled = true; btn.textContent = "Adding…"; }
  try {
    const res = await fetch("/api/cart/add", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ id })
    });
    const data = await res.json();
    if (data.success) {
      updateCartDot(data.cart_count);
      showToast("🍦 " + data.message);
      if (btn) {
        btn.textContent = "✓ Added!";
        btn.style.background = "#6BCB77";
        setTimeout(() => {
          btn.textContent = "🛒 Add to Cart";
          btn.style.background = "";
          btn.disabled = false;
        }, 1600);
      }
    }
  } catch (e) {
    if (btn) { btn.textContent = "🛒 Add to Cart"; btn.disabled = false; }
  }
}

function updateCartDot(count) {
  const navCart = document.querySelector(".nav-cart");
  let dot = document.querySelector(".cart-dot");
  if (count > 0) {
    if (dot) { dot.textContent = count; }
    else if (navCart) {
      dot = document.createElement("span");
      dot.className = "cart-dot";
      dot.textContent = count;
      navCart.appendChild(dot);
    }
  } else {
    if (dot) dot.remove();
  }
}

function showToast(msg) {
  const t = document.getElementById("toast");
  if (!t) return;
  t.textContent = msg;
  t.classList.add("show");
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => t.classList.remove("show"), 2800);
}
