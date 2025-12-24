// /home/MiguelAeTxio/CampuStudiOnline/static/js/tours/academic_structure_explorer_helpers.js
// Helper functions for the admin academic structure explorer.

function copyPrompt(taskId) {
  const textarea = document.getElementById('prompt-' + taskId);
  const button = document.getElementById('copy-btn-' + taskId);
  const buttonText = button.querySelector('.text');

  const originalText = 'Copy';
  const successText = 'Copied!';

  if (!textarea || !button || !buttonText) {
    console.error('Elements not found for task:', taskId);
    return;
  }

  textarea.focus();
  textarea.select();
  textarea.setSelectionRange(0, textarea.value.length);

  let successful = false;
  try {
    successful = document.execCommand('copy');
  } catch (err) {
    console.error('Error trying to execute document.execCommand:', err);
    successful = false;
  }

  if (successful) {
    button.disabled = true;
    buttonText.innerText = successText;
    button.classList.add('is-copied');

    setTimeout(() => {
      buttonText.innerText = originalText;
      button.classList.remove('is-copied');
      button.disabled = false;
    }, 2000);
  } else {
    console.error('Could not copy text to clipboard.');
  }

  if (window.getSelection) {
    if (window.getSelection().empty) {  // Standard
      window.getSelection().empty();
    } else if (window.getSelection().removeAllRanges) {  // Firefox
      window.getSelection().removeAllRanges();
    }
  } else if (document.selection) {  // IE
    document.selection.empty();
  }
}
