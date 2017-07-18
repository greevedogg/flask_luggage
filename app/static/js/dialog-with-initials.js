;(function(window){
    'use strict';

    var DialogWithInitials = function(config) {
        var acceptLabel = config.buttonAccept;
        var acceptCallback = config.acceptCallback;
        var partyName = '';

        var $myModal = $('#myModal');

        $myModal.on('show.bs.modal', function(e) {
            $("#dialog__close-ticket__party-name").text(partyName);
        });

        $('.dialog__close-ticket__close').text(acceptLabel);
        $('.modal-title').html(this.titleTemplate);

        var $form = $('.modal-dialog form');
        $form.validate({
            rules: {
                'dialog__close-ticket-initials': {
                    required: true,
                    minlength: 2,
                    maxlength: 3
                }
            }
        });

        $('.dialog__close-ticket__close').on('click touchstart', function(event) {
            event.preventDefault();

            var initials = $('#dialog__close-ticket-initials').get(0);
            $form.validate();
            
            if ($form.valid()) {
                $myModal.modal('hide');
                initials.setCustomValidity('');
                
                ga('send', 'event', 'luggage', 'archive');
                
                acceptCallback();
            }
        });

        function show() {
            $myModal.modal('show');
        }

        function hide() {
            $myModal.modal('hide');
        }

        function setParty(name) {
            partyName = name;
        }

        return {
            show: show,
            hide: hide,
            setParty: setParty
        };
    };

    // different titles, different button labels
    // I need to know if the dialog was accepted or dismissed
    window.DialogWithInitials = DialogWithInitials;
})(window);

(function(window){
    'use strict';

    var CloseTicketDialog = function(){
        return DialogWithInitials.apply(this, arguments);
    };

    CloseTicketDialog.prototype = _.create(DialogWithInitials.prototype, {
        'constructor': CloseTicketDialog,
        'titleTemplate': 'Close ticket for <span id="dialog__close-ticket__party-name">&nbsp;</span> party?'

    });

    window.CloseTicketDialog = CloseTicketDialog;
})(window);

(function(window){
    'use strict';

    var ModifyTicketDialog = function(){
        return DialogWithInitials.apply(this, arguments);
    };

    ModifyTicketDialog.prototype = _.create(DialogWithInitials.prototype, {
        'constructor': ModifyTicketDialog,
        'titleTemplate': 'Modify ticket for <span id="dialog__close-ticket__party-name">&nbsp;</span> party?'

    });

    window.ModifyTicketDialog = ModifyTicketDialog;
})(window);
