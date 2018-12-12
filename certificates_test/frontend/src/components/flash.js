function isFlash() {
  var flashObject = document.getElementById('flash-msg-box');
  if (flashObject !== null) {
    return true;
  }
  else {
    return false;
  }
}

function removeFlash() {
  var flashObject = document.getElementById('flash-msg-box');
  var removeFlashBtn = document.getElementById('delete-flash-btn');
  var modalBg = document.getElementById('flash-msg-background');
  removeFlashBtn.onclick = function() {
    flashObject.remove();
  }
  modalBg.onclick = function() {
    flashObject.remove();
  }
}

isFlash = isFlash();
if (isFlash == true) {
  removeFlash();
}

function switchModal() {
  var modalAnchor = document.getElementById('about-test-mechanism-anchor-button');
  var modalObject = document.getElementById('about-test-mechanism');
  var removeModalBtn = document.getElementById('delete-modal-btn');
  var modalBg = document.getElementById('modal-background');
  modalAnchor.onclick = function() {
    modalObject.classList.add('is-active');
  }
  removeModalBtn.onclick = function() {
    modalObject.classList.remove('is-active');
  }
  modalBg.onclick = function() {
    modalObject.classList.remove('is-active');
  }
}
switchModal();
