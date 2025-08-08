export const hasPermission = (user, permissionName) => {
    return user && user.perfil && user.perfil.permissoes.some(p => p.nome === permissionName);
};