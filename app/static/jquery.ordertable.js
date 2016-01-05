/**
	- Only works with vertical tables, headings on top.
	- Order according to cells contents
	- To customize order, you can specify a data-ordertable-value on each <td>. Eg.: <td data-ordertable-value="1425333217">Monday, 02 March 2015</td>
	- force table ordering (on col 2, asc) : $('.myTable').orderTable('order', {column: 2, order:"asc"});
	- excludeRows $('tr:first-chid')...
*/
(function($) {
	// OrderTable object
	var OrderTable = {};

	/**
		initialize object; calls initTable on targets
	*/
	OrderTable.init = function($target, options) {
		// options
		if(options && !isNaN(options.excludeColumns) && options.excludeColumns%1===0) {
			options.excludeColumns = [options.excludeColumns];
		}
		OrderTable.options = $.extend({}, {
			buttonClass: "order-table",
			buttonAscClass: "order-table--asc",
			buttonDescClass: "order-table--desc",
			excludeRows: null,	// excluded rows are always on top ($(...), must be a <tr>)
			excludeColumns: []	// excluded columns (0-based indexes) cannot be ordered
		}, options);
		// $target must contain only table(s) !
		$target.each(function(){
			if($target.is('table')) {
				OrderTable.initTable($(this));
			}
		});
		// return jquery object
		return $target;
	};

	/**
		initTable
	*/
	OrderTable.initTable = function($table) {
		var o = OrderTable.options;
		var $headings = $('th', $table);
		for(var i in o.excludeColumns) {
			if(o.excludeColumns[i] < 0) {
				o.excludeColumns[i] = $headings.length + o.excludeColumns[i];
			}
		}
		$headings = $headings.filter(function(index){
			for (var i = 0; i < o.excludeColumns.length; i++) {
				if (o.excludeColumns[i] == index) {
					return false;
				}
			}
			return true;
		});
		$table.data("$headings", $headings);
		// add ordering buttons
		$headings.addClass(o.buttonClass).click(OrderTable.orderToggle);
	};

	OrderTable.orderToggle = function() {
		var o = OrderTable.options;
		var $headings = $(this).closest('table').data('$headings');
		var isAsc = $(this).hasClass(o.buttonAscClass);
		$headings.removeClass(o.buttonAscClass).removeClass(o.buttonDescClass);
		$(this).addClass(isAsc ? o.buttonDescClass : o.buttonAscClass);
		return OrderTable.order(this, isAsc); // now order by desc if button *was* "ASC"
	}
	OrderTable.orderAsc = function() {
		return OrderTable.order(this);
	};
	OrderTable.orderDesc = function() {
		return OrderTable.order(this, true);
	};
	OrderTable.order = function(that, orderDesc) {
		var colIndex = $(that).closest('th').index();
		var $table = $(that).closest('table');		
		return OrderTable.orderColumn($table, colIndex, orderDesc);
	};

	OrderTable.orderColumn = function($table, colIndex, orderDesc) {
		var $cells = $('td:nth-child(' + (colIndex + 1) + ')', $table);
		// loop through cells of this column
		$cells.sort(function(a, b){
			// take the data-xxx value if present
			var aDataValue = $(a).attr("data-ordertable-value");
			var bDataValue = $(b).attr("data-ordertable-value");
			var aStr = (typeof aDataValue === "undefined") ? (a.innerText || a.textContent) : aDataValue;
			var bStr = (typeof bDataValue === "undefined") ? (b.innerText || b.textContent) : bDataValue;
			var aInt = parseInt(aStr);
			var bInt = parseInt(bStr);
			// order factor (-1 if desc)
			var f = orderDesc ? -1 : 1;
			// order (excluded rows always before)
			var e = OrderTable.options.excludeRows;
			if(e && $(a).closest(e).length) {
				return -1;
			} else if(e && $(b).closest(e).length) {
				return 1;
			} else if(isNaN(aInt) || isNaN(bInt)) {
				return aStr.localeCompare(bStr) * f;
			} else {
				return (aInt - bInt) * f;
			}
		});
		// reorder DOM
		$cells.each(function(){
			$table.append($(this).closest('tr'));
		})
		return false;
	};

	/*
		actions
	*/
	OrderTable.actionOrder = function(actionParams) {
		actionParams = actionParams || {};
		var colIndex = actionParams.column;
		var orderDesc = actionParams.order==='desc';
		if(isNaN(colIndex)) {
			return;
		}
		OrderTable.orderColumn(this, colIndex, orderDesc);
	}

	// actions (called by $(..).orderTable("action"))
	OrderTable.actions = {
		'order': OrderTable.actionOrder
	};

	// jquery extension (can take options object or action string as parameter)
	$.fn.extend({
		orderTable: function(optionsOrAction, actionParams) {
			// if string => action
			if(typeof(optionsOrAction) === "string" && typeof(OrderTable.actions[optionsOrAction] === "function")) {
				OrderTable.actions[optionsOrAction].call(this, actionParams);
				return this;
			}
			// else => init
			return OrderTable.init(this, optionsOrAction);
		}
	});
}(jQuery));