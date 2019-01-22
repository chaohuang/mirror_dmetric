General options
---------------

\begin{longtable}{p{3cm}p{2cm}p{8cm}}
\hline
{\bf Parameter }  & {\bf Value} & {\bf Usage} \\ \hline
  --help           & 0   & This help text                                      \\ \hline
  --fileA          & ""  & Input file 1, original version                      \\ \hline
  --fileB          & ""  & Input file 2, processed version                     \\ \hline
  --inputNorm      & ""  & File name to import the normals of original point   \\ 
                   &     & cloud, if different from original file 1n           \\ \hline
  --singlePass     & 0   & Force running a single pass, where the loop is      \\ 
                   &     & over the original point cloud                       \\ \hline
  --hausdorff      & 0   & Send the Haursdorff metric as well                  \\ \hline
  --color          & 0   & Check color distortion as well                      \\ \hline
  --lidar          & 0   & Check lidar reflectance as well                     \\ \hline
  --resolution     & 0   & Specify the intrinsic resolution                    \\ \hline
  --dropdups       & 2   & 0(detect), 1(drop), 2(average) subsequent points    \\ 
                   &     & with same coordinates                               \\ \hline
  --neighborsProc  & 1   & 0(undefined), 1(average), 2(weighted average),      \\ 
                   &     & 3(min), 4(max) neighbors with same geometric        \\ 
                   &     & distance                                            \\ \hline
  --averageNormals & 1   & 0(undefined), 1(average normal based on neighbors   \\ 
                   &     & with same geometric distance)                       \\ \hline
  --nbThreads      & 1   & Number of threads used for parallel processing      \\ \hline
\end{longtable}

                               
