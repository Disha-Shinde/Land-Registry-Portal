
function validate_form(formid) {
	var form = document.getElementById(formid);
	for(var i=0; i < form.elements.length; i++){
	  if(form.elements[i].value === '' && form.elements[i].hasAttribute('required')){
		alert('Please fill all the * marked fields!');
		return false;
	  }
	}
	form.submit();
};

	