/**
 * Created by James on 07/12/2015.
 */
$(document).ready(function() {
    var $table = $('.table');
    //Make a clone of our table
    var $fixedColumn = $table.clone().insertBefore($table).addClass('fixed-column');

    //Remove everything except for first column
    $fixedColumn.find('th:nth-child(n+4),td:nth-child(n+4)').remove();

    //Match the height of the rows to that of the original table's
    $fixedColumn.find('tr').each(function (i, elem) {
        $(this).height($table.find('tr:eq(' + i + ')').height());
    });
});