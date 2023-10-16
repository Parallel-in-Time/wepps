# Web Development Documentation

## Development

The frontend is built using Typescript and uses vite as a build tool.
The backend uses by default the latest build of vite, i.e., the single Javascript file, if the `enforce_dev_mode` flag in `web.py` isn't set such as `Site(..., enforce_dev_mode=True)`.
To use the latest Typescript files (if anything was changed and wasn't build yet), one has to set the flag and start the vite development server.

For this go into the `frontend` folder and enter

```sh
yarn
yarn dev
```

and start the backend from the base project directory in another terminal with

```
python web.py
```

## Building

The project can be built inside the `wepps/frontend` folder with

```sh
yarn
yarn build
```

The files created this way will automatically be picked up by the frontend and are used by default.
