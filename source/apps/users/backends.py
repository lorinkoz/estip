# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ldap.functions import initialize as ldap_init

from .models import User
from apps.students.models import Student

SERVER_UHO = 'ldap://10.26.0.39:389'
SERVER_CSM = 'ldap://10.26.32.5:389'

DOMAINS = {
    'fh.uho.edu.cu': SERVER_CSM,
    'facinf.uho.edu.cu': SERVER_UHO,
    'facing.uho.edu.cu': SERVER_UHO,
    'facii.uho.edu.cu': SERVER_UHO,
    'ict.uho.edu.cu': SERVER_UHO,
    'vrea.uho.edu.cu': SERVER_UHO,
    'vru.uho.edu.cu': SERVER_UHO,
}


def lcs(string1, string2):
    l1, l2 = len(string1), len(string2)
    if not l1 or not l2:
        return 0
    matrix = [0 for x in range(l1*l2)]
    lcs = 0
    for i in range(1, l1):
        for e in range(1, l2):
            index = i * l2 + e
            diag = (i-1) * l2 + (e-1)
            upper = (i-1) * l2 + e
            left = i * l2 + (e-1)
            if string1[i] == string2[e]:
                matrix[index] = matrix[diag] + 1
            else:
                matrix[index] = max(matrix[upper], matrix[left])
            lcs = max(matrix[index], lcs)
    return lcs


def match_student(full_name):
    max_lcs = 0
    student = None
    full_name = full_name.lower()
    student_map = [(x, x.full_name.lower()) for x in Student.objects.all()]
    for this_student, student_full_name in student_map:
        match_rate = lcs(student_full_name, full_name)
        if match_rate > max_lcs and match_rate / float(len(student_full_name)) > 0.8:
            max_lcs = match_rate
            student = this_student
    return student


class OpenLdapUHOBackend():

    def get_user(self, id):
        return User.objects.filter(pk=id).first()

    def authenticate(self, username=None, password=None):
        email = username
        try:
            # Retrieve domain from email
            domain = username.split('@')[1]
            # Get the LDAP server based on email domain
            ldap_server = DOMAINS.get(domain, None)
            if not ldap_server:
                return None
            # Bind anonymously to search for the DN
            ldapc = ldap_init(ldap_server)
            r = ldapc.bind('', '')
            r = ldapc.search('dc=uho,dc=edu,dc=cu', 2, 'mail=%s' % email, [b'givenName', b'sn'])
            raw_data = ldapc.result(r)
            ldap_dn = raw_data[1][0][0]
            data = raw_data[1][0][1]
            # Bind with retrived DN and password
            r = ldapc.bind(ldap_dn, password)
            ldapc.result(r)
            ldapc.unbind()
            # At this point user authenticated successfully in LDAP server
        except:
            return None
        # Extract name and surname from LDAP retrieved data
        ldap_first_name = data.get('givenName', ['']).pop().strip()
        ldap_last_name = data.get('sn', ['']).pop().strip()
        # Get the user from database, if exists
        user = User.objects.filter(email=email).first()
        # If user is found, we update and return it
        if user:
            user.display_name = ' '.join([ldap_first_name, ldap_last_name]).strip()
            user.set_password(password)
            user.save()
            return user
        # If user is not found, we then try to match the name and surname with
        # an existing student, to create a consultor linked to that student
        ldap_full_name = ' '.join([ldap_first_name, ldap_last_name]).strip()
        student = match_student(ldap_full_name)
        # If no proper match is found, we return None
        if not student:
            return None
        # Otherwise we consider the authenticated user to be this student <<<<<<< TRULY?????
        # So we create the new user
        user = User(email=email, display_name=' '.join([ldap_first_name, ldap_last_name]).strip(), role=1)
        user.set_password(password)
        user.save()
        # Then we assign the new user to the target student
        student.linked_user = user
        student.save()
        # And we finally return the user
        return user
