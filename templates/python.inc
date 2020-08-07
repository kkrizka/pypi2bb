HOMEPAGE = "{{homepage}}"
SUMMARY = "{{summary}}"
LICENSE = "{{license}}"
LIC_FILES_CHKSUM = "file://{{licname}};md5={{licmd5}}"

SRC_URI[md5sum] = "{{md5sum}}"
SRC_URI[sha256sum] = "{{sha256sum}}"

{%- if realname is not none %}
BPN="{{realname}}"
{%- endif %}
{% if pkgext != "tar.gz" %}
PYPI_PACKAGE_EXT="{{pkgext}}"
{% endif %}

inherit pypi

{%- if depends|length > 0 %}
DEPENDS += " \
  {%- for depend in depends %}
    ${PYTHON_PN}-{{depend}}-native \
  {%- endfor %}
"
{%- endif %}

{%- if rdepends|length > 0 %}
RDEPENDS_${PN} += " \
  {%- for rdepend in rdepends %}
    ${PYTHON_PN}-{{rdepend}} \
  {%- endfor %}
"
{%- endif %}
