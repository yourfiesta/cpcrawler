
var firstGrid = new ax5.ui.grid();
var mask = new ax5.ui.mask();

$(document).ready(function(){
    
    //csrf_token을 위한 setup
    var csrftoken = getCookie('csrftoken');
        $.ajaxSetup({
          beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
              xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
          }
        });
    
    setGrid();
    setDataPicker();
    
    $("#searchBtn").click(function(){
        loadData();
    })
    
    //오늘날짜 세팅
    var date = new Date();
    var nowDate = date.getFullYear() + '-' + fn_leadingZeros(date.getMonth() + 1, 2) + '-' + fn_leadingZeros(date.getDate(), 2);
    $("#endDate").val(nowDate);
    
    nowDate = nowDate.split("-");
    var beforeDate = new Date();
    beforeDate.setFullYear(nowDate[0], nowDate[1]-1, nowDate[2]-7);
    var y = beforeDate .getFullYear();
    var m = beforeDate.getMonth() + 1;
    var d = beforeDate.getDate();

    if(m < 10) { m = "0" + m; }
    if(d < 10) { d = "0" + d; }
    beforeDate = y + "-" + m + "-" + d;
   
    $("#startDate").val(beforeDate);
    loadData();
    
});

function setDataPicker(){
    //datepicker 설정
    $.datepicker.regional['ko'] = {
        closeText: '닫기',
        prevText: '이전달',
        nextText: '다음달',
        currentText: '오늘',
        monthNames: ['1월(JAN)','2월(FEB)','3월(MAR)','4월(APR)','5월(MAY)','6월(JUN)',
        '7월(JUL)','8월(AUG)','9월(SEP)','10월(OCT)','11월(NOV)','12월(DEC)'],
        monthNamesShort: ['1월','2월','3월','4월','5월','6월',
        '7월','8월','9월','10월','11월','12월'],
        dayNames: ['일','월','화','수','목','금','토'],
        dayNamesShort: ['일','월','화','수','목','금','토'],
        dayNamesMin: ['일','월','화','수','목','금','토'],
        weekHeader: 'Wk',
        dateFormat: 'yy-mm-dd',
        firstDay: 0,
        isRTL: false,
        showMonthAfterYear: true,
        yearSuffix: '',
        showOn: 'both',
        buttonText: "달력",
        changeMonth: true,
        changeYear: true,
        showButtonPanel: true,
        yearRange: 'c-99:c+99',
    };
    $.datepicker.setDefaults($.datepicker.regional['ko']);
 
    $('#startDate').datepicker();
    $('#startDate').datepicker("option", "maxDate", $("#startDate").val());
    $('#startDate').datepicker("option", "onClose", function ( selectedDate ) {
        $("#endDate").datepicker( "option", "minDate", selectedDate );
    });
 
    $('#endDate').datepicker();
    $('#endDate').datepicker("option", "minDate", $("#sdate").val());
    $('#endDate').datepicker("option", "onClose", function ( selectedDate ) {
        $("#startDate").datepicker( "option", "maxDate", selectedDate );
    });
}



function setGrid(){
	//ax5ui-grid 설정
	
	 
    firstGrid.setConfig({
        target: $('[data-ax5grid="first-grid"]'),
        header: {
            align: "center",
            columnHeight: 30
        },
        sortable: true,
        columns: [
            {key: "stt_de", label: "날짜", align: "center", width:100,
            	formatter: function(){
            		var yy = this.value.substring(0,4);
            		var mm = this.value.substring(4,6);
            		var dd = this.value.substring(6,8);
            		
            		return yy + "-" + mm + "-" + dd
            	}},
            {key: "stt_tm", label: "시간", align: "center", width:80,
        		formatter: function(){
        			var tt = this.value.substring(0,2);
            		var mm = this.value.substring(2,4);
            		
            		return tt + ":" + mm
        		}},
            {key: "keyword", label: "키워드"},
            {key: "rk", label: "순위", align: "center", width:50},
            {key: "title", label: "제품명", width: 450},
            {key: "price", label: "가격(원)", align: "right",
            	formatter: function(){
            		return this.value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
            	}}
        ],
        showLineNumber: true,
        showRowSelector: true,
        multipleSelect: true,
        lineNumberColumnWidth: 40,
        rowSelectorColumnWidth: 27,
    });

    
}

function loadData(){
	var keyword = $("#keyword").val();
    var startDate = $("#startDate").val().replace(/-/gi, "");
    var endDate = $("#endDate").val().replace(/-/gi, "");
    
    if(startDate != "" && endDate != ""){
        
    	mask.setConfig({
            target: $("#first-grid").get(0),
            content: "<h1>Loading..</h1>",
            zIndex: 40,
            onStateChanged: function(){
            	
            }
        });
    	
    	mask.open({
    		theme: 'gray',
    		content: '<h1><i class="fa fa-spinner fa-spin"></i> Loading</h1>'
        });
    	
        $.ajax({
        data: {
           'keyword': keyword,
           'startDate': startDate,
           'endDate': endDate,
        },
        type: 'post',
        dataType: 'json',
        url: '/getJsonData/',
        success: function(data){
            
             firstGrid.setData(data);
             mask.close();
        }
    });
    }
}



function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
          var cookies = document.cookie.split(';');
          for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
            }
          }
        }
        return cookieValue;
      }
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function fn_leadingZeros(n, digits) {

	  var zero = '';

	  n = n.toString();

	  if (n.length < digits) {

	    for (var i = 0; i < digits - n.length; i++){ zero += '0'; }

	  }

	  return zero + n;

}