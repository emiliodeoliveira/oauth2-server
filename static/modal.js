var btn = document.querySelector('#showModal');
var modalDlg = document.querySelector('#image-modal');
var imageModalCloseBtn = document.querySelector('#image-modal-close');
var closeBtn = document.querySelector('#closeBtn');
btn.addEventListener('click', function(){
  modalDlg.classList.add('is-active');
});

imageModalCloseBtn.addEventListener('click', function(){
  modalDlg.classList.remove('is-active');
});
closeBtn.addEventListener('click', function(){
  modalDlg.classList.remove('is-active');
});

