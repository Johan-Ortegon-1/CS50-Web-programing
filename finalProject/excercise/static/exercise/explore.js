document.addEventListener('DOMContentLoaded', function() {
	if(document.getElementById("tg_btn_review"))
	{
		document.getElementById('tg_btn_review').addEventListener('click', switchExploreView);
		switchExploreView();
	}
	document.getElementById('btn_show_filters').addEventListener('click', showFilters);
}, false);

function switchExploreView(e) {
	const toggle = document.getElementById('tg_btn_review');
	if(toggle.checked)
	{
		document.querySelector('#review_section').style.display = 'flex';
		document.querySelector('#approved_section').style.display = 'none';
	}
	else
	{
		document.querySelector('#review_section').style.display = 'none';
		document.querySelector('#approved_section').style.display = 'flex';
	}
}

function showFilters(e){
	document.getElementById('filters').classList.toggle("filter-container-show");
}