

$( document ).ready(function() {
	
	$('#extrainfo-table').DataTable({
	  "iDisplayLength": 25,
	  "bPaginate": false,
   	  "bInfo": false,
   	  "bFilter": false,
   	  "order": [[ 0, "desc" ]],
   	  "columnDefs": [
   	          { type: 'time-uni', targets: 1 }, 
   	          { type: 'time-uni', targets: 2 }
   	        ]
    });
});
