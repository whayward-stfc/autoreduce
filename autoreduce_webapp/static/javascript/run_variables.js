(function(){
    var formUrl = $('#run_variables').attr('action');

    var previewScript  = function previewScript(event){
        var submitAction = function submitAction(){
            var url = $('#preview_url').val();
            var $form = $('#run_variables');
            if($form.length===0) $form = $('#instrument_variables');
            $form.attr('action', url);
            window.onbeforeunload = undefined;
            $form.submit();
        };
        var cancelAction = function cancelAction(){
            return false;
        };
        event.preventDefault();
        if(validateForm()){
            checkForConflicts(submitAction);
        }else{
            cancelAction();
        }
    };

    var validateForm = function validateForm(){
        var isValid = true;
        var $form = $('#run_variables');
        if($form.length===0) $form = $('#instrument_variables');

        var resetValidationStates = function resetValidationStates(){
            $('.has-error').removeClass('has-error');
        };

        var validateRunRange = function validateRunRange(){
            var $start = $('#run_start');
            var $end = $('#run_end');
            if($start.length && $end.length){
                validateNotEmpty.call($start[0]);
                if(!isNumber($start.val())){
                    $start.parent().addClass('has-error');
                    isValid = false;
                }
                if($end.val() !== '' && !isNumber($end.val())){
                    $end.parent().addClass('has-error');
                    isValid = false;
                }
                if(parseInt($end.val()) < parseInt($start.val())){
                    $end.parent().addClass('has-error');
                    isValid = false;
                }
            }
        };

        var validateNotEmpty = function validateNotEmpty(){
            if($(this).val().trim() === ''){
                $(this).parent().addClass('has-error');
                isValid = false;
            }
        };
        var validateText = function validateText(){
            validateNotEmpty.call(this);
        };
        var validateNumber = function validateNumber(){
            validateNotEmpty.call(this);
            if(!isNumber($(this).val())){
                $(this).parent().addClass('has-error');
                isValid = false;
            }
        };
        var validateBoolean = function validateBoolean(){
            validateNotEmpty.call(this);
            if($(this).val().toLowerCase() !== 'true' && $(this).val().toLowerCase() !== 'false'){
                $(this).parent().addClass('has-error');
                isValid = false;
            }
        };
        var validateListNumber = function validateListNumber(){
            var items, i;
            validateNotEmpty.call(this);
            if($(this).val().trim().endsWith(',')){
                $(this).parent().addClass('has-error');
                isValid = false;
            }else{
                items = $(this).val().split(',');
                for(i=0;i<items.length;i++){
                    if(!isNumber(items[i])){
                        $(this).parent().addClass('has-error');
                        isValid = false;
                        break;
                    }
                }
            }
        };
        var validateListText = function validateListText(){
            var items, i;
            validateNotEmpty.call(this);
            if($(this).val().trim().endsWith(',')){
                $(this).parent().addClass('has-error');
                isValid = false;
            }else{
                items = $(this).val().split(',');
                for(i=0;i<items.length;i++){
                    if(items[i].trim() === ''){
                        $(this).parent().addClass('has-error');
                        isValid = false;
                        break;
                    }
                }
            }
        };

        // Populate all boolean values with their checked state
        $('[data-type="boolean"]').each(function(){
            if($(this).attr('checked')){
                $(this).val('True');
            }else{
                $(this).val('False');
            }
        });

        resetValidationStates();
        validateRunRange();
        $('[data-type="text"]').each(validateText);
        $('[data-type="number"]').each(validateNumber);
        $('[data-type="boolean"]').each(validateBoolean);
        $('[data-type="list_number"]').each(validateListNumber);
        $('[data-type="list_text"]').each(validateListText);

        return isValid;
    };

    var triggerAfterRunOptions = function triggerAfterRunOptions(){
        if($(this).val().trim() !== ''){
            $('#next_run').text(parseInt($(this).val())+1);
            $('#run_finish_warning').show();
        }else{
            $('#run_finish_warning').hide();
        }
    };

    var showDefaultSriptVariables = function showDefaultSriptVariables(){
        $('#default-variables-modal').modal();
    };

    var checkForConflicts = function checkForConflicts(successCallback){
        var start = parseInt($('#run_start').val());
        var end = parseInt($('#run_end').val());
        var conflicts = [];
        if($('#upcoming_runs').length > 0){
            var upcoming = $('#upcoming_runs').val().split(',');
            for(var i=0;i<upcoming.length;i++){
                if(parseInt(upcoming[i]) >= start && (end == NaN || upcoming[i] <= end)){
                    conflicts.push(upcoming[i]);
                }
            }
        }
        if(conflicts.length === 0){
            successCallback();
        }else{
            $('.js-conflicts-list').text(conflicts.join(','));
            $('#conflicts-modal .js-conflicts-confirm').unbind('click').on('click', successCallback);
            $('#conflicts-modal').modal();
        }
    };

    var submitForm = function submitForm(event){
        var submitAction = function submitAction(){
            var $form = $('#run_variables');
            if($form.length===0) $form = $('#instrument_variables');
            $form.attr('action', formUrl);
            window.onbeforeunload = undefined;
            $form.submit();
        };
        var cancelAction = function cancelAction(){
            return false;
        };

        event.preventDefault();
        if(validateForm()){
            checkForConflicts(submitAction);
        }else{
            cancelAction();
        }
    };

    var restrictFinished = function restrictFinished(){
        var $end = $('#run_end');
        var $start = $('#run_start');
        var setMin = function setMin(){
            $end.attr('min', $start.val());
        };        
        $start.on('change', setMin);
        setMin();
    };

    var confirmUnsavedChanges = function confirmUnsavedChanges(){
        var $form = $('#run_variables');
        if($form.length===0) $form = $('#instrument_variables');

        $form.on('change', function(){
            $form.unbind('change');
            window.onbeforeunload = function confirmLeave(event) {
                if(!event) event = window.event;
                event.cancelBubble = true;
                event.returnValue = 'There are unsaved changes.';
                if (event.stopPropagation) {
                    event.stopPropagation();
                    event.preventDefault();
                }
            };

        });
    };

    var resetDefaultVariables = function resetDefaultVariables(event){
        event.preventDefault();
        var $form = $('#run_variables');
        if($form.length===0) $form = $('#instrument_variables');
        $form.html($('#default_instrument_variables_form').html());
        // We need to enable the popover again as the element is new
        $('[data-toggle="popover"]').popover();
    };

    var cancelForm = function cancelForm(event){
        event.preventDefault();
        window.onbeforeunload = undefined;
        window.location.href = document.referrer;
    };
    
    var init = function init(){
        $('#run_variables,#instrument_variables').on('click', '#previewScript', previewScript);
        $('#run_variables,#instrument_variables').on('click', '#resetValues', resetDefaultVariables);
        $('#run_variables,#instrument_variables').on('click', '#variableSubmit', submitForm);
        $('#run_variables,#instrument_variables').on('click', '#cancelForm', cancelForm);
        $('#run_end').on('change', triggerAfterRunOptions);
        $('.js-show-default-variables').on('click', showDefaultSriptVariables);
        restrictFinished();
        confirmUnsavedChanges();
    };

    init();
}())