# Copyright 2014 Ahmed H. Ismail

#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at

#        http://www.apache.org/licenses/LICENSE-2.

#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
from .. import utils
class InvalidDocumentError(Exception):

    """Raised if attempting to write an invalid document."""
    pass


def write_seperators(out):
    for i in xrange(0, 4):
        out.write('\n')

def write_value(tag, value, out):
    out.write('{0}: {1}\n'.format(tag, value))

def write_text_value(tag, value, out):
    text_value = '<text>{0}</text>'.format(value)
    write_value(tag, text_value, out)


def write_creation_info(creation_info, out):
    """Writes out the creation info, does not check if it's valid."""
    out.write('# Creation Info\n\n')
    # Write creators
    for creator in creation_info.creators:
        write_value('Creator', creator, out)
    # write created
    write_value('Created', creation_info.created_iso_format, out)
    # possible comment
    if creation_info.has_comment:
        write_text_value('CreatorComment', creation_info.comment, out)


def write_review(review, out):
    """Writes out the fields of a single review in tag/value format."""
    out.write('# Review\n\n')
    write_value('Reviewer', review.reviewer, out)
    write_value('ReviewDate', review.review_date_iso_format, out)
    if review.has_comment:
        write_text_value('ReviewComment', review.comment, out)


def write_file(file, out):
    pass

def write_package(package, out):
    """Writes out the fields of a package in tag/value format."""
    out.write('# Package\n\n')
    write_value('PackageName', package.name, out)
    if package.has_optional_field('version'):
        write_value('PackageVersion', package.version, out)
    write_value('PackageDownloadLocation', package.download_location, out)
    if package.has_optional_field('summary'):
        write_text_value('PackageSummary', package.summary, out)
    if package.has_optional_field('source_info'):
        write_text_value('PackageSourceInfo', package.source_info, out)
    if package.has_optional_field('file_name'):
        write_value('PackageFileName', package.file_name, out)
    if package.has_optional_field('supplier'):
        write_value('PackageSupplier', package.supplier, out)
    if package.has_optional_field('originator'):
        write_value('PackageOriginator', package.originator, out)
    if package.has_optional_field('check_sum'):
        write_value('PackageChecksum', package.check_sum, out)
    write_value('PackageVerificationCode', package.verif_code, out)
    if package.has_optional_field('description'):
        write_text_value('PackageDescription', package.description, out)
    write_value('PackageLicenseDeclared', package.license_declared, out)
    write_value('PackageLicenseConcluded', package.conc_lics, out)
    # Write list of licenses.
    for lics in package.licenses_from_files:
        write_value('PackageLicenseInfoFromFiles', lics, out)
    if package.has_optional_field('license_comment'):
        write_text_value('PackageLicenseComments', package.license_comment, out)
    # cr_text is either free form text or NONE or NOASSERTION.
    if isinstance(package.cr_text, str):
        write_text_value('PackageCopyrightText', package.cr_text, out)
    else:
        write_value('PackageCopyrightText', package.cr_text, out)
    if package.has_optional_field('homepage'):
        write_value('PackageHomePage', package.homepage, out)
    # Write files.
    for file in package.files:
        write_file(file, out)

    



def write_extr_licens(lics, out):
    pass


def write_document(document, out):
    """Writes out a tag value representation of the document.
    Out must implement a method write that takes a single string.
    """
    if not document.validate():
        raise InvalidDocumentError()
    # Write out document information
    out.write('# Document Information\n\n')
    version_value = 'SPDX-{0}.{1}'.format(document.version.major, 
                                            document.version.minor)
    write_value('SPDXVersion', version_value, out)
    write_value('DataLicense', document.data_license.identifier, out)
    if document.has_comment:
        write_text_value('DocumentComment', document.comment, out)
    write_seperators(out)
    # Write out creation info
    write_creation_info(document.creation_info, out)
    write_seperators(out)
    # Write out reviews
    for review in document.reviews:
        write_review(review, out)
        write_seperators(out)
    # Write out package info
    write_package(document.package, out)
    write_seperators(out)
    for lic in document.extracted_licenses:
        write_extr_licens(lic)
        write_seperators(out)
