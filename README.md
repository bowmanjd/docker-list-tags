# docker-list-tags

Python script to list image tags for a given repository in a given registry.

Also includes functionality to filter the list of image tags and obtain the tag naming the latest version, using a regular expression pattern. The script does not interact with the commonly-used yet confusing `latest` tag.

# Use cases

A common use case: automated building and publishing of container images that depend on other container images.

For instance, suppose you desire to publish and evergreen Alpine-based container image that tracks the latest version of Alpine available on Docker Hub. It may be helpful, in such a case, to poll the source for the latest version, then build and tag as appropriate.

## Dependencies

This script requires Python. Other than those included in the Python Standard Library, no other libraries are necessary.

## Alternatives

[Skopeo] is a great command line tool for container manipulation. It includes a `skopeo list-tags` command that achieves similar goals to this project.

## Contributing

Feel free to open an issue if you have suggestions, questions, or glowing affirmations.

## Copyright and License

Copyright © 2021 Jonathan Bowman. All documentation and code contained in these files may be freely shared in compliance with the [Apache License, Version 2.0][license] and is **provided “AS IS” without warranties or conditions of any kind**.

[article]: https://dev.to/bowmanjd/
[license]: LICENSE
[apachelicense]: http://www.apache.org/licenses/LICENSE-2.0
[skopeo]: https://github.com/containers/skopeo
