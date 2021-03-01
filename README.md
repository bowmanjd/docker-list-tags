# docker-list-tags

Python script to get the name of the latest version of a container image from a Docker (or other) registry.

The script does not interact with the commonly-used `latest` tag. Instead, a regular expression pattern is used to determine which tags bear version numbers. By default, this filters out tags that do not have numbers and dots ("`.`"). The maximum version number in the list is then considered the latest and returned.

# Use cases

A common use case: automated building and publishing of container images that depend on other container images.

For instance, suppose you desire to publish and evergreen Alpine-based container image that tracks the latest version of Alpine available on Docker Hub. It may be helpful, in such a case, to poll the source for the latest version, then build and tag as appropriate.

## Dependencies

This script requires [Skopeo] to be installed first.

## Contributing

Feel free to open an issue if you have suggestions, questions, or glowing affirmations.

## Copyright and License

Copyright © 2021 Jonathan Bowman. All documentation and code contained in these files may be freely shared in compliance with the [Apache License, Version 2.0][license] and is **provided “AS IS” without warranties or conditions of any kind**.

[article]: https://dev.to/bowmanjd/
[license]: LICENSE
[apachelicense]: http://www.apache.org/licenses/LICENSE-2.0
[skopeo]: https://github.com/containers/skopeo
