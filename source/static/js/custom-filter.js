
var includePage = false;

// Changes page
function changePage(page) {
	if (page > 1) includePage = true;
	$("[name=p]", "#filter").val(page.toString());
	$("#filter").submit();
}

// Cleans and submits a filter form
function submitFilter(evt, data){
	evt.preventDefault();
	args = "";
	
	fields = $("[name]","#filter").not("[type=submit]").not("[type=button]");
	if (!includePage) fields = fields.not("[name=p]");
	for (i = 0; i < fields.length; i++) {
		fields[i].disabled = true;
		if (fields[i].value) {
			args += args?"&":"?";
			args += fields[i].name + "=" + fields[i].value;
		}
	}
	
	location.href = location.pathname + args;
}

$(function(){
	$("form#filter").submit(submitFilter);
	console.log(location.search)
	if (location.search) {
		$("[name=q]", "form#filter").focus()
	}
});