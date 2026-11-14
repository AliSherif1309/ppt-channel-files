# PPT Channel Files

GitHub Pages builds the presentation index using Jekyll. Presentation content is
stored in Git LFS; downloads use GitHub's media host to resolve actual files.
Folder ZIPs preserve paths, report unavailable files, and limit uncompressed
content to 200 MiB per download. Use smaller subfolders for large collections.

On Windows enable long paths for this checkout with `git config core.longpaths true`.
Use Git LFS when downloading the library. The website lists only PowerPoint files.
