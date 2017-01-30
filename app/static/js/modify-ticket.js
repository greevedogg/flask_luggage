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
        
        function openConfirmDialog(event) {
            var val = $modifiedBy.val();

            if (val == '') {
                modifyTicketDialog.setParty($('#name').val());
                modifyTicketDialog.show();
            } else {
                console.log('This is supposed to submit');
            }
        }

        $('#submit').on('click', openConfirmDialog);
        
        $("#form-edit-ticket input").keyup(function(event){
            if(event.keyCode == 13){
            	openConfirmDialog(event);
            }
        });
    });
})();
