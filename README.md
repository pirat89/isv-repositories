# isv-repositories

This is a place where ISVs can contribute their [Leapp repositories](https://leapp.readthedocs.io/en/latest/terminology.html#repository) to enable and enhance the upgradeability of their applications.

The directory structure for this repository is as follows:
```
upgrade_type/vendor/product/...
```

For example, the ACME Corp. will end up with this structure for their ACME Storage product
for inplace upgrade from RHEL 7 to RHEL 8:
```
el7toel8/acme/acme_storage/{actors,models}
```

If you're interested in contributing, please read the [Contributor Guidelines](https://github.com/oamg/leapp-guidelines/blob/master/contributing-guidelines.rst)
