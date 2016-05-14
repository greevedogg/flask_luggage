;(function(){
    'use strict';

    $(function(){
        var $modifiedBy = $('#modifiedBy');

        var modifyTicketDialog = new ModifyTicketDialog({
            buttonAccept: 'Modify Ticket',
            acceptCallback: function() {
                modifyTicketDialog.hide();
                var initials = $('#dialog__close-ticket-initials').val();

                $modifiedBy.val(initials);

                $('#form-edit-ticket').submit();
            }
        });

        $('#submit').on('click', function(event) {
            var val = $modifiedBy.val();

            if (val == '') {
                modifyTicketDialog.setParty($('#name').val());
                modifyTicketDialog.show();
            } else {
                console.log('This is supposed to submit');
            }
        });
    });
})();
