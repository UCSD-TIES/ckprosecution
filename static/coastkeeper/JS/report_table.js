jQuery.fn.dataTableExt.oSort['bool-asc'] = function (a, b) {
    if ($(a).hasClass('glyphicon-ok') && $(b).hasClass('glyphicon-remove')) {
        return -1
    } else if ($(a).hasClass('glyphicon-remove') && $(b).hasClass('glyphicon-ok')) {
        return 1
    }
    else return 0
};

jQuery.fn.dataTableExt.oSort['bool-desc'] = function (a, b) {
    if ($(a).hasClass('glyphicon-ok') && $(b).hasClass('glyphicon-remove')) {
        return 1
    } else if ($(a).hasClass('glyphicon-remove') && $(b).hasClass('glyphicon-ok')) {
        return -1
    }
    else return 0
};

$.fn.dataTableExt.afnFiltering.push(
    function (oSettings, aData, iDataIndex) {
        if ($('#datepicker_start').val() != '' || $('#datepicker_end').val() != '') {
            var iMin_temp = $('#datepicker_start').val();
            if (iMin_temp == '') {
                iMin_temp = '1980-01-01';
            }
            var iMax_temp = $('#datepicker_end').val();
            if (iMax_temp == '') {
                iMax_temp = '2024-01-01';
            }

            var arr_min = iMin_temp.split("-");
            var arr_max = iMax_temp.split("-");
            var arr_date = aData[0].split("-");

            var iMin = new Date(arr_min[0], arr_min[1], arr_min[2], 0, 0, 0, 0)
            var iMax = new Date(arr_max[0], arr_max[1], arr_max[2], 0, 0, 0, 0)
            var iDate = new Date(arr_date[0], arr_date[1], arr_date[2], 0, 0, 0, 0)

            if (iMin == "" && iMax == "") {
                return true;
            }
            else if (iMin == "" && iDate < iMax) {
                return true;
            }
            else if (iMin <= iDate && "" == iMax) {
                return true;
            }
            else if (iMin <= iDate && iDate <= iMax) {
                return true;
            }
        }
        else
            return true
    }
);