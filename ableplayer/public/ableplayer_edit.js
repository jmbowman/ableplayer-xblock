/* Javascript for AblePlayerXBlock. */
function AblePlayerXBlock(runtime, element) {

    function updateCount(result) {
        $('.count', element).text(result.count);
    }

    $(function ($) {
        /* Here's where you'd do things on page load. */
        console.log('HELLO WORLD');
        $('.ableplayer-edit').on('click', '.add-caption', function (e) {
            console.log('add caption clicked');
        });
    });
};

function AblePlayerEdit(runtime, element) {
    function successMessage() {
        console.log('success!');
    }

    // function processInputs(inputArray) {
    //     return inputArray.reduce((memo, val) => {
    //         if ((val.name).indexOf('_') > 0) {
    //             var components = val.name.split('_'),
    //                 key = components[0] + '_files',
    //                 contents = {
    //                     'filepath'
    //                 };

    //             if (!memo[key]) {
    //                 memo[key] = [];
    //             }
    //             memo[key].append(contents);
    //         } else {
    //             memo[val.name] = val.value;
    //         }
    //         return memo;
    //     }, {});
    // }

    function serializeData($form) {
        var serializedData = {
            title: $form.find('.title').val(),
            filepath: $form.find('.filepath').val()
        };

        $form.find('.text-track-inputs').each(function(index) {
            var $inputWrappers = $(this).find('.input-wrapper');
            if ($inputWrappers.length > 0) {
                var key = $(this).data('inputType') + '_files';
                var myArr = [];
                $inputWrappers.each(function(index) {
                    var item = {};
                    item.filepath = $(this).find('.input-filepath').val();
                    item.language = $(this).find('.input-language').val();
                    if (item.filepath) {
                        myArr.push(item);
                    }
                });
                if (myArr.length) {
                    serializedData[key] = myArr;
                }
            }
        });
        return serializedData;
    }

    $('.ableplayer-edit').on('click', '.add-input', function (e) {
        e.preventDefault();
        var container = $(e.target).parent().find('.input-container'),
            inputType = $(e.target).parent().data('inputType'),
            displayInputType = inputType.charAt(0).toUpperCase() + inputType.slice(1),
            currentIndex = container.find('input-wrapper').length;

        container.append(
            '<div class="input-wrapper">' +
            '<label>' + displayInputType + ' Filepath ' +
            '<input type="text" class="input-filepath" value="" name="' + inputType + '_' + currentIndex + '_filepath" />' +
            '</label><label>' + displayInputType + ' Language ' +
            '<input type="text" class="input-language" value="" name="' + inputType + '_' + currentIndex + '_language" />' +
            '</label></div>'
        );
    });

    $('.ableplayer-video-meta').on('submit', function(e) {
        e.preventDefault();
        var handlerUrl = runtime.handlerUrl(element, 'edit_video_fields');

        // var serializedData = JSON.stringify(processInputs(JSON.parse(JSON.stringify($( this ).serializeArray()))));
        var serializedData = serializeData($(this));
        console.log(serializedData);

        $.ajax({
            type: "POST",
            url: handlerUrl,
            data: JSON.stringify(serializedData),
            success: successMessage
        });
    });
}
