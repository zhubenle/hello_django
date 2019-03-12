let users_obj = {
    csrfToken: $("[name=csrfmiddlewaretoken]").val(),
    urlPageUsers: $('#url_page_users').val(),
    urlPageRoles: $('#url_page_roles').val(),
    urlAddUser: $('#url_add_user').val(),
    urlUpdateUser: $('#url_update_user').val(),
    urlObtainUser: $('#url_obtain_user').val(),
    tableUsers: null,

    usernameRegex: new RegExp('[a-zA-Z0-9_]{8,20}'),
    passwordRegex: new RegExp('\\S{8,32}'),
    realNameRegex: new RegExp('\\S{2,}'),
    emailRegex: new RegExp('^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\\.[a-zA-Z0-9_-]+)+$'),
    phoneRegex: new RegExp('^1[34578]\\d{9}$'),

    addInputUsername: $('#add_input_username'),
    addInputPassword: $('#add_input_password'),
    addInputCfmPassword: $('#add_input_cfm_password'),
    addInputRealName: $('#add_input_real_name'),
    addInputEmail: $('#add_input_email'),
    addInputPhone: $('#add_input_phone'),
    addSelectRoles: $('#add_select_roles'),
    modalAdd: $('#modal_add'),
    addSelectRolesSelect2: null,

    editInputUsername: $('#edit_input_username'),
    editInputPassword: $('#edit_input_password'),
    editInputCfmPassword: $('#edit_input_cfm_password'),
    editInputRealName: $('#edit_input_real_name'),
    editInputEmail: $('#edit_input_email'),
    editInputPhone: $('#edit_input_phone'),
    editSelectRoles: $('#edit_select_roles'),
    modalEdit: $('#modal_edit'),
    editSelectRolesSelect2: null,
    editUserId: null,

    init: function (_opt) {
        users_obj.tableUsers = $('#table_users').DataTable({
            serverSide: true,
            processing: true,
            searching: true,
            autoWidth: false,
            language: {
                lengthMenu: 'Show _MENU_'
            },
            searchDelay: 2000,
            ajax: {
                url: users_obj.urlPageUsers,
                type: 'POST',
                data: {csrfmiddlewaretoken: users_obj.csrfToken},
                dataFilter: function (resp) {
                    resp = $.parseJSON(resp);
                    if (resp.code === 10000) {
                        return JSON.stringify(resp.data);
                    }
                    return JSON.stringify({'error': resp.msg});
                }
            },
            createdRow: function (tr, data, dataIndex, tds) {
                let append_html = '<td><button class="btn btn-primary btn-sm" onclick="users_obj.show_edit_modal(' + data.id + ', this)">Edit User</button></td>';
                $(tr).append(append_html);
            },
            columns: [
                {data: 'id'},
                {data: 'username'},
                {data: 'real_name'},
                {data: 'phone'},
                {data: 'email'},
                {data: 'last_login_ip', searchable: false},
                {data: 'last_login_time', searchable: false},
                {data: 'update_time', searchable: false},
                {data: 'create_time', searchable: false},
                {
                    data: 'del_status',
                    searchable: false,
                    createdCell: function (td, cellData, rowData, row, col) {
                        let style = cellData ? 'label-danger' : 'label-info';
                        $(td).html('<lable class="label ' + style + '">' + cellData + '</lable>');
                    }
                }
            ],
        });

        let rolesSelect2Option = {
            placeholder: 'Select roles',
            maximumSelectionLength: 1,
            delay: 300,
            allowClear: true,
            cache: true,
            ajax: {
                url: users_obj.urlPageRoles,
                method: 'POST',
                dataType: 'JSON',
                data: function (params) {
                    let start = (params.page ? params.page - 1 : 0) * 10;
                    let term = params.term ? params.term : '';
                    return {
                        start: start,
                        'columns[1][data]': 'name',
                        'columns[1][searchable]': 'true',
                        'columns[1][search][value]': term.toUpperCase(),
                        csrfmiddlewaretoken: users_obj.csrfToken
                    }
                },
                processResults: function (resp, params) {
                    if (resp.code === 10000) {
                        params.page = params.page || 1;
                        return {
                            "results": $.map(resp.data.data, function (role) {
                                return {
                                    "id": role.id,
                                    "text": role.name
                                }
                            }),
                            "pagination": {
                                "more": 10 * params.page < resp.data.recordsTotal
                            }
                        }
                    } else {
                        return null;
                    }
                }
            }
        };

        users_obj.addSelectRolesSelect2 = users_obj.addSelectRoles.select2(rolesSelect2Option);


        users_obj.modalAdd.on('hidden.bs.modal', function (e) {
            users_obj.add_clear();
        });

        users_obj.editSelectRolesSelect2 = users_obj.editSelectRoles.select2(rolesSelect2Option);

        users_obj.modalEdit.on('hidden.bs.modal', function (e) {
            users_obj.edit_clear();
        });
    },
    add_validate: function () {
        //验证添加用户或者编辑用户时输入的表单数据
        let is_submit = true;
        let username = users_obj.addInputUsername.val();
        if (!users_obj.usernameRegex.test(username)) {
            users_obj.addInputUsername.parents('.form-group').addClass('has-error')
                .find('span > i').addClass('fa-times');
            is_submit = false;
        }
        let password = users_obj.addInputPassword.val();
        if (!users_obj.passwordRegex.test(password)) {
            users_obj.addInputPassword.parents('.form-group').addClass('has-error')
                .find('span > i').addClass('fa-times');
            is_submit = false;
        }
        let cfm_password = users_obj.addInputCfmPassword.val();
        if (cfm_password !== password) {
            users_obj.addInputCfmPassword.parents('.form-group').addClass('has-error')
                .find('span > i').addClass('fa-times');
            is_submit = false;
        }
        let real_name = users_obj.addInputRealName.val();
        if (!users_obj.realNameRegex.test(real_name)) {
            users_obj.addInputRealName.parents('.form-group').addClass('has-error')
                .find('span > i').addClass('fa-times');
            is_submit = false;
        }
        let email = users_obj.addInputEmail.val();
        if (email.length > 64 || !users_obj.emailRegex.test(email)) {
            users_obj.addInputEmail.parents('.form-group').addClass('has-error')
                .find('span > i').addClass('fa-times');
            is_submit = false;
        }
        let phone = users_obj.addInputPhone.val();
        if (!users_obj.phoneRegex.test(phone)) {
            users_obj.addInputPhone.parents('.form-group').addClass('has-error')
                .find('span > i').addClass('fa-times');
            is_submit = false;
        }
        let roles = users_obj.addSelectRolesSelect2.val();
        if (!roles || roles.length < 1) {
            users_obj.addSelectRoles.parents('.form-group').addClass('has-error')
                .find('span > i').addClass('fa-times');
            is_submit = false;
        }
        return {
            is_submit: is_submit,
            username: username,
            password: password,
            real_name: real_name,
            email: email,
            phone: phone,
            roles: roles,
        };
    },
    add_user: function (btn) {
        //添加用户
        let result = users_obj.add_validate();
        if (result.is_submit) {
            $(btn).attr('disabled', 'disabled');
            $.ajax(users_obj.urlAddUser, {
                method: 'POST',
                dataType: 'JSON',
                data: {
                    csrfmiddlewaretoken: users_obj.csrfToken,
                    username: result.username,
                    password: result.password,
                    real_name: result.real_name,
                    email: result.email,
                    phone: result.phone,
                    roles: result.roles.join(',')
                },
                success: function (resp) {
                    if (resp.code === 10000) {
                        users_obj.modalAdd.modal('hide');
                        swal('Success', 'User add success', 'success').then(function () {
                            users_obj.tableUsers.draw();
                        });
                    } else {
                        swal('Fail', 'User add fail: ' + resp.msg, 'error')
                    }
                },
                error: function (xhr, ts, et) {
                    swal('Fail', 'User add error: ' + et, 'error');
                },
                complete: function () {
                    $(btn).removeAttr('disabled')
                }
            });
        }
    },
    add_clear: function () {
        //清空添加模态框中的数据
        users_obj.addInputUsername.val('');
        users_obj.addInputPassword.val('');
        users_obj.addInputCfmPassword.val('');
        users_obj.addInputRealName.val('');
        users_obj.addInputEmail.val('');
        users_obj.addInputPhone.val('');
        users_obj.addSelectRolesSelect2.val(null).trigger('change');
        users_obj.modalAdd.find('.form-group').removeClass('has-error').removeClass('has-success')
            .find('span > i').removeClass('fa-times').removeClass('fa-check')
    },
    show_edit_modal: function (id, btn) {
        //显示编辑用户的modal
        $(btn).attr('disabled', 'disabled');
        users_obj.editUserId = id;

        $.ajax(users_obj.urlObtainUser, {
            method: 'POST',
            dataType: 'JSON',
            data: {
                csrfmiddlewaretoken: users_obj.csrfToken,
                id: id
            },
            success: function (resp) {
                if (resp.code === 10000) {
                    users_obj.editInputUsername.val(resp.data.username);
                    users_obj.editInputPassword.val(resp.data.password);
                    users_obj.editInputCfmPassword.val(resp.data.password);
                    users_obj.editInputRealName.val(resp.data.real_name);
                    users_obj.editInputEmail.val(resp.data.email);
                    users_obj.editInputPhone.val(resp.data.phone);
                    $.each(resp.data.roles, function (i, role) {
                        users_obj.editSelectRolesSelect2.append(new Option(role.name, role.id, true, true))
                    });
                    users_obj.editSelectRolesSelect2.trigger('change');
                    users_obj.modalEdit.find('input[name="del_status"][value="' + resp.data.del_status + '"]').prop('checked', true);
                    users_obj.modalEdit.modal('show');
                } else {
                    swal('Fail', 'User obtain fail: ' + resp.msg, 'error')
                }
            },
            error: function (xhr, ts, et) {
                swal('Fail', 'User obtain error: ' + et, 'error');
            },
            complete: function () {
                $(btn).removeAttr('disabled');
            }
        });
    },
    edit_validate: function () {
        //验证添加用户或者编辑用户时输入的表单数据
        let is_submit = true;
        let username = users_obj.editInputUsername.val();
        if (!users_obj.usernameRegex.test(username)) {
            users_obj.editInputUsername.parents('.form-group').addClass('has-error')
                .find('span > i').addClass('fa-times');
            is_submit = false;
        }
        let password = users_obj.editInputPassword.val();
        if (!users_obj.passwordRegex.test(password)) {
            users_obj.editInputPassword.parents('.form-group').addClass('has-error')
                .find('span > i').addClass('fa-times');
            is_submit = false;
        }
        let cfm_password = users_obj.editInputCfmPassword.val();
        if (cfm_password !== password) {
            users_obj.editInputCfmPassword.parents('.form-group').addClass('has-error')
                .find('span > i').addClass('fa-times');
            is_submit = false;
        }
        let real_name = users_obj.editInputRealName.val();
        if (!users_obj.realNameRegex.test(real_name)) {
            users_obj.editInputRealName.parents('.form-group').addClass('has-error')
                .find('span > i').addClass('fa-times');
            is_submit = false;
        }
        let email = users_obj.editInputEmail.val();
        if (!users_obj.emailRegex.test(email)) {
            users_obj.editInputEmail.parents('.form-group').addClass('has-error')
                .find('span > i').addClass('fa-times');
            is_submit = false;
        }
        let phone = users_obj.editInputPhone.val();
        if (!users_obj.phoneRegex.test(phone)) {
            users_obj.editInputPhone.parents('.form-group').addClass('has-error')
                .find('span > i').addClass('fa-times');
            is_submit = false;
        }
        let roles = users_obj.editSelectRolesSelect2.val();
        if (!roles || roles.length < 1) {
            users_obj.editSelectRoles.parents('.form-group').addClass('has-error')
                .find('span > i').addClass('fa-times');
            is_submit = false;
        }
        let del_status = users_obj.modalEdit.find('input[name="del_status"]:checked').val();
        return {
            is_submit: is_submit,
            id: users_obj.editUserId,
            username: username,
            password: password,
            real_name: real_name,
            email: email,
            phone: phone,
            roles: roles,
            del_status: del_status,
        };
    },
    edit_user: function (btn) {
        //更新用户
        let result = users_obj.edit_validate();
        if (result.is_submit) {
            $(btn).attr('disabled', 'disabled');
            $.ajax(users_obj.urlUpdateUser, {
                method: 'POST',
                dataType: 'JSON',
                data: {
                    csrfmiddlewaretoken: users_obj.csrfToken,
                    id: result.id,
                    username: result.username,
                    password: result.password,
                    real_name: result.real_name,
                    email: result.email,
                    phone: result.phone,
                    roles: result.roles.join(','),
                    del_status: result.del_status
                },
                success: function (resp) {
                    if (resp.code === 10000) {
                        users_obj.modalEdit.modal('hide');
                        swal('Success', 'User edit success', 'success').then(function () {
                            users_obj.tableUsers.draw();
                        });
                    } else {
                        swal('Fail', 'User edit fail: ' + resp.msg, 'error')
                    }
                },
                error: function (xhr, ts, et) {
                    swal('Fail', 'User edit error: ' + et, 'error');
                },
                complete: function () {
                    $(btn).removeAttr('disabled');
                }
            });
        }
    },
    edit_clear: function () {
        //清空编辑模态框中的数据
        users_obj.editInputUsername.val('');
        users_obj.editInputPassword.val('');
        users_obj.editInputCfmPassword.val('');
        users_obj.editInputRealName.val('');
        users_obj.editInputEmail.val('');
        users_obj.editInputPhone.val('');
        users_obj.editSelectRolesSelect2.val(null).trigger('change');
        users_obj.modalEdit.find('.form-group').removeClass('has-error').removeClass('has-success')
            .find('span > i').removeClass('fa-times').removeClass('fa-check');
        users_obj.modalEdit.find('input[name="del_status"]').removeProp('checked');
    }
};